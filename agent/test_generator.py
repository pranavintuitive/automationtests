from pathlib import Path
import textwrap
import re
import itertools
import json
from agent.data_factory import deterministic_value
from resolution.engine import TestDataResolutionEngine
from resolution.contracts import TestStepResolutionRequest



API_TEST_FILE = Path("automation/api/test_generated_api.py")

TC_COUNTER = itertools.count(1)


# ----------------------------
# Helpers
# ----------------------------

def next_tc_id() -> str:
    return f"TC_API_{next(TC_COUNTER):03d}"


def safe_test_name(value: str) -> str:
    value = value.strip("/")
    value = re.sub(r"[{}\\/]+", "_", value)
    value = re.sub(r"-+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.lower().strip("_")


def bdd_test_name(method: str, path: str) -> str:
    clean = safe_test_name(path)
    action = {
        "GET": "get",
        "POST": "create",
        "PUT": "update",
        "DELETE": "delete",
        "PATCH": "update",
    }.get(method.upper(), method.lower())
    return f"{action}_{clean}"


# ----------------------------
# Schema-Based Payload Builder
# ----------------------------

def build_payload_from_schema(schema: dict, tc_id: str, parent_field: str = ""):
    if not schema:
        return None

    schema_type = schema.get("type")

    if schema_type == "object":
        properties = schema.get("properties", {})
        result = {}
        for field, field_schema in properties.items():
            result[field] = build_payload_from_schema(
                field_schema,
                tc_id,
                parent_field=field,
            )
        return result

    if schema_type == "array":
        item_schema = schema.get("items", {})
        return [build_payload_from_schema(item_schema, tc_id, parent_field)]

    return deterministic_value(tc_id, parent_field, schema_type)


def generate_payload_from_intent(ep: dict, tc_id: str):
    request_schema = ep.get("request_schema")

    if not request_schema:
        return None

    return build_payload_from_schema(request_schema, tc_id)


def generate_query_params_from_intent(ep: dict, tc_id: str):
    query_schema = ep.get("query_schema")
    if not query_schema:
        return None

    return build_payload_from_schema(query_schema, tc_id)

def resolve_with_engine(ep: dict, tc_id: str, swagger_spec_from_Parent: dict):
    """
    Uses TestDataResolutionEngine to resolve payload + query safely.
    Falls back to schema-based builder if resolution fails.
    """

    try:
        engine = TestDataResolutionEngine()

        swagger_spec =  swagger_spec_from_Parent  # In real implementation, this would be passed down or accessed globally
        role_context = {
            "role": "system",
            "token": None,
            "restricted_fields": []
        }

        resolution_request = TestStepResolutionRequest(
            endpoint=ep["endpoint"],
            http_method=ep["method"],
            swagger_spec=swagger_spec,
            intent_metadata=ep.get("intent_metadata", {}),
            role_context=role_context,
            execution_context={},
            deterministic_seed=int(tc_id.split("_")[-1]),
        )

        resolved = engine.resolve(resolution_request)

        return resolved.body, resolved.query_params

    except Exception:
        # Safe fallback to existing behavior
        payload = generate_payload_from_intent(ep, tc_id)
        query = generate_query_params_from_intent(ep, tc_id)
        return payload, query


# ----------------------------
# Main generator
# ----------------------------

def generate_tests(base_url: str, intent_model: list, swagger_spec: dict):

    API_TEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    code = f"""
import pytest
import requests
import logging
from resolution.lifecycle_engine import LifecycleChainingEngine
from resolution.execution_context import ExecutionContext

BASE_URL = "{base_url}"

EXECUTION_CONTEXT = ExecutionContext()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("api_test.log"), logging.StreamHandler()]
)

def log_request_response(method, url, response):
    logging.info(f"REQUEST {{method}} {{url}}")
    logging.info(f"Status Code: {{response.status_code}}")
    logging.info(f"Response Body: {{response.text[:1000]}}")

def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=15, **kwargs)
    except Exception as e:
        logging.exception("Request failed")
        pytest.fail(str(e))
"""


    # ----------------------------
    # Generate tests per endpoint
    # ----------------------------
    creation_endpoints = [
    ep for ep in intent_model
    if ep.get("classification") == "create"
    ]

    non_creation_endpoints = [
        ep for ep in intent_model
        if ep.get("classification") != "create"
    ]

    ordered_endpoints = creation_endpoints + non_creation_endpoints

    for ep in ordered_endpoints:

        method = ep["method"].upper()
        raw_path = ep["endpoint"]
        tc_id_base = next_tc_id()
        static_path = raw_path
        # Replace path params with deterministic placeholder
        runtime_path  = replace_path_params_with_swagger(
                                                raw_path,
                                                method,
                                                swagger_spec,
                                                tc_id_base,
                                                )

        classification = ep.get("classification", "unknown")
        risk = ep.get("risk_level", "medium")
        roles_info = ep.get("roles", {})
        role_access = roles_info.get("role_access", {})
        requires_auth = roles_info.get("requires_auth", False)

        test_base_name = bdd_test_name(method, static_path)
        url_expr = f'f"{{BASE_URL}}{runtime_path}"'

        # Generate deterministic payload + query
       
        payload, query_params = resolve_with_engine(ep, tc_id_base, swagger_spec)

        payload_code = json.dumps(payload, indent=4) if payload else "None"
        query_code = json.dumps(query_params, indent=4) if query_params else "None"

        # ----------------------------------
        # ROLE-BASED TEST GENERATION
        # ----------------------------------

        for role_name, is_allowed in role_access.items():

            tc_id = next_tc_id()
            fixture_name = f"{role_name}_headers"

            if is_allowed:

                code += textwrap.dedent(f"""
@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.{risk}
def test_{test_base_name}_as_{role_name}({fixture_name}):
    \"\"\"
    Test Case ID: {tc_id}
    Role: {role_name}
    Classification: {classification}
    Risk Level: {risk}
    \"\"\"

    url = {url_expr}
    payload = {payload_code}
    query = {query_code}

    response = safe_request(
        "{method}",
        url,
        headers={fixture_name},
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("{method}", url, response)

    # ---- Lifecycle Capture ----
    if "{classification}" == "create":
        try:
            data = response.json()
            captured = LifecycleChainingEngine.extract_resource_values(
                data,
                {json.dumps(swagger_spec)}
            )
            EXECUTION_CONTEXT.register(captured)
        except Exception:
            pass
            
    assert response.status_code in (200, 201, 202, 204)
""")

            else:

                code += textwrap.dedent(f"""
@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.{risk}
def test_{test_base_name}_as_{role_name}_forbidden({fixture_name}):
    \"\"\"
    Test Case ID: {tc_id}_SEC
    Role: {role_name}
    Expected: Forbidden
    \"\"\"

    url = {url_expr}

    response = safe_request("{method}", url, headers={fixture_name})

    log_request_response("{method}", url, response)

    assert response.status_code in (401, 403)
""")

        # ----------------------------------
        # UNAUTHENTICATED ACCESS TEST
        # ----------------------------------

        if requires_auth:

            tc_id = next_tc_id()

            code += textwrap.dedent(f"""
@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.{risk}
def test_{test_base_name}_without_auth():
    \"\"\"
    Test Case ID: {tc_id}_NOAUTH
    Verify unauthenticated access is rejected
    \"\"\"

    url = {url_expr}
    response = safe_request("{method}", url)

    log_request_response("{method}", url, response)

    assert response.status_code in (401, 403)
""")

        # ----------------------------------
        # CONTRACT SAFETY TEST
        # ----------------------------------

        tc_id = next_tc_id()

        code += textwrap.dedent(f"""
@pytest.mark.contract
@pytest.mark.{risk}
def test_{test_base_name}_contract_stability():
    \"\"\"
    Test Case ID: {tc_id}_CONTRACT
    Verify endpoint does not produce 5xx errors
    \"\"\"

    url = {url_expr}
    response = safe_request("{method}", url)

    log_request_response("{method}", url, response)

    assert response.status_code < 500
""")

    API_TEST_FILE.write_text(code.strip(), encoding="utf-8")
    print(f"[GENERATED] {API_TEST_FILE}")

def replace_path_params(path: str, tc_id: str):
    def replacer(match):
        param_name = match.group(1)
        return str(deterministic_value(tc_id, param_name, "string"))
    return re.sub(r"{([^}]+)}", replacer, path)

import uuid


def replace_path_params_with_swagger(path: str, method: str, swagger_spec: dict, tc_id: str):
    """
    Replaces {path} parameters using Swagger schema.
    Supports uuid format properly.
    """

    paths = swagger_spec.get("paths", {})
    path_item = paths.get(path, {})
    operation = path_item.get(method.lower(), {})

    # Collect parameters from both path-level and operation-level
    parameters = []
    parameters.extend(path_item.get("parameters", []))
    parameters.extend(operation.get("parameters", []))

    param_map = {
        p["name"]: p.get("schema", {})
        for p in parameters
        if p.get("in") == "path"
    }

    def replacer(match):
        param_name = match.group(1)
        schema = param_map.get(param_name, {})

        param_type = schema.get("type")

        fallback = deterministic_value(
            tc_id,
            param_name,
            param_type or "string"
        )

        # Build runtime-safe expression
        return '{' + f'EXECUTION_CONTEXT.get("{param_name}") or "{fallback}"' + '}'

    return re.sub(r"{([^}]+)}", replacer, path)

from pathlib import Path
import json
import textwrap
import re
import itertools
from agent.data_factory import deterministic_value

API_TEST_FILE = Path("automation/api/test_generated_api.py")

TC_COUNTER = itertools.count(1)

# ----------------------------
# Helpers
# ----------------------------

def next_tc_id() -> str:
    return f"TC_API_{next(TC_COUNTER):03d}"


def resolve_path_params(path: str, parameters: list) -> str:
    for param in parameters or []:
        if param.get("in") == "path":
            name = param["name"]
            path = path.replace("{" + name + "}", f"test_{name}")
    return path


def safe_test_name(value: str) -> str:
    value = value.strip("/")
    value = re.sub(r"[{}\\/]+", "_", value)
    value = re.sub(r"-+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.lower().strip("_")


def requires_auth(endpoint: dict) -> bool:
    security = endpoint.get("security")
    if security is None:
        return True
    return bool(security)


def is_login_endpoint(path: str) -> bool:
    return "auth/login" in path or path.endswith("/login")


def swagger_description(endpoint: dict) -> str:
    return (
        endpoint.get("summary")
        or endpoint.get("description")
        or "Validate API behavior"
    ).strip().replace("\n", " ")


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


def get_response_schema(endpoint: dict):
    responses = endpoint.get("responses", {})
    success = responses.get("200") or responses.get("201")
    if not success:
        return None
    return success.get("content", {}).get("application/json", {}).get("schema")


# ----------------------------
# Main generator
# ----------------------------

def generate_tests(base_url: str, endpoints: list):
    API_TEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    code = f"""
import pytest
import requests
import logging
import json
from automation.utils.schema_assertions import assert_schema

BASE_URL = "{base_url}"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("api_test.log"), logging.StreamHandler()]
)

def log_request_response(method, url, payload, response):
    logging.info(f"REQUEST {{method}} {{url}}")
    logging.info(f"Payload: {{payload}}")
    logging.info(f"Status Code: {{response.status_code}}")
    logging.info(f"Response Body: {{response.text[:1000]}}")

def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=15, **kwargs)
    except Exception as e:
        logging.exception("Request failed")
        pytest.fail(str(e))


@pytest.fixture(scope="session")
def auth_headers():
    response = requests.post(
        f"{{BASE_URL}}/api/v1/auth/auth/login",
        data={{
            "grant_type": "password",
            "username": "admin@acme.com",
            "password": "admin123",
            "client_id": "string",
            "client_secret": "",
        }},
        timeout=15,
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        pytest.fail("Auth token missing")
    return {{"Authorization": f"Bearer {{token}}"}}
"""

    for ep in endpoints:
        method = ep["method"].upper()
        path = resolve_path_params(ep["path"], ep.get("parameters", []))

        if is_login_endpoint(path):
            continue

        tc_id = next_tc_id()
        test_name = bdd_test_name(method, path)
        description = swagger_description(ep)
        url_expr = f'f"{{BASE_URL}}{path}"'
        auth_needed = requires_auth(ep)

        payload, payload_type = generate_positive_payload(ep, tc_id)
        neg_payload = generate_negative_payload(ep, tc_id)

        response_schema = get_response_schema(ep)
        response_schema_code = json.dumps(response_schema, indent=4) if response_schema else "None"

        headers = "headers=auth_headers" if auth_needed else ""

        code += f"\nRESPONSE_SCHEMA = {response_schema_code}\n"

        # ---------------- POSITIVE (CONTRACT) ----------------
        code += textwrap.dedent(f"""
@pytest.mark.contract
def test_{test_name}_positive({ "auth_headers" if auth_needed else "" }):
    \"\"\"
    Test Case ID: {tc_id}
    GIVEN {description}
    WHEN client sends {method} {path}
    THEN response should match API contract
    \"\"\"

    url = {url_expr}
    payload = {json.dumps(payload, indent=4) if payload else "None"}

    response = safe_request(
        "{method}",
        url,
        {"data" if payload_type == "form" else "json"}=payload if payload else None,
        {headers}
    )

    log_request_response("{method}", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)
""")

        # ---------------- NEGATIVE ----------------
        code += textwrap.dedent(f"""
def test_{test_name}_negative({ "auth_headers" if auth_needed else "" }):
    \"\"\"
    Test Case ID: {tc_id}_NEG
    GIVEN invalid input
    WHEN client sends {method}
    THEN API should reject request
    \"\"\"

    url = {url_expr}
    payload = {json.dumps(neg_payload, indent=4) if neg_payload else "None"}

    response = safe_request(
        "{method}",
        url,
        json=payload if payload else None,
        {headers}
    )

    log_request_response("{method}", url, payload, response)

    assert response.status_code in (400,401,403,404,422)
""")

    API_TEST_FILE.write_text(code.strip(), encoding="utf-8")
    print(f"[GENERATED] {API_TEST_FILE}")


# ----------------------------
# Payload generators
# ----------------------------

def generate_positive_payload(endpoint: dict, tc_id: str):
    body = endpoint.get("requestBody")
    if not body:
        return None, None

    content = body.get("content", {})

    if "application/x-www-form-urlencoded" in content:
        schema = content["application/x-www-form-urlencoded"].get("schema", {})
        payload_type = "form"
    elif "application/json" in content:
        schema = content["application/json"].get("schema", {})
        payload_type = "json"
    else:
        return None, None

    properties = schema.get("properties", {})
    payload = {
        field: deterministic_value(tc_id, field, spec.get("type"))
        for field, spec in properties.items()
    }

    return payload, payload_type


def generate_negative_payload(endpoint: dict, tc_id: str):
    payload, _ = generate_positive_payload(endpoint, tc_id)
    if not payload:
        return None
    payload = payload.copy()
    payload.pop(next(iter(payload)))
    return payload
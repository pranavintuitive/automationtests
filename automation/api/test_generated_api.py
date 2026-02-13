import pytest
import requests
import logging
from resolution.lifecycle_engine import LifecycleChainingEngine
from resolution.execution_context import ExecutionContext

BASE_URL = "http://34.56.161.228:8000/"
EXECUTION_CONTEXT = ExecutionContext()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("api_test.log"), logging.StreamHandler()]
)

def log_request_response(method, url, response):
    logging.info(f"REQUEST {method} {url}")
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response Body: {response.text[:1000]}")

def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=15, **kwargs)
    except Exception as e:
        logging.exception("Request failed")
        pytest.fail(str(e))


@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_auth_auth_login_as_admin(admin_headers):
    """
    Test Case ID: TC_API_002
    Role: admin
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/auth/auth/login"
    payload = {
    "grant_type": "password",
    "username": "admin@acme.com",
    "password": "admin123",
    "scope": "",
    "client_id": "",
    "client_secret": ""
}
    query = None

    response = safe_request(
        "POST",
        url,
        headers=admin_headers,
        data=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_auth_auth_login_as_user(user_headers):
    """
    Test Case ID: TC_API_003
    Role: user
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/auth/auth/login"
    payload = {
    "grant_type": "password",
    "username": "user@acme.com",
    "password": "user123",
    "scope": "",
    "client_id": "",
    "client_secret": ""
}
    query = None

    response = safe_request(
        "POST",
        url,
        headers=user_headers,
        data=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.high
def test_create_api_v1_auth_auth_login_contract_stability():

    url = f"{BASE_URL}/api/v1/auth/auth/login"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_start_as_admin(admin_headers):
    """
    Test Case ID: TC_API_006
    Role: admin
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    payload = {
    "product_idea": "product_idea_771",
    "domain": "domain_5033",
    "target_audience": {
        "primary": [
            "primary_7842"
        ],
        "secondary": [
            "secondary_9905"
        ]
    },
    "documentation_objective": "documentation_objective_7763",
    "regulatory_context": [
        "regulatory_context_7419"
    ],
    "job_id": "40f15e7c-933b-5e10-aa69-82550e6faa32"
}
    query = None

    response = safe_request(
        "POST",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_start_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    response = safe_request("POST", url, headers=user_headers)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_start_without_auth():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_start_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_approve_as_admin(admin_headers):
    """
    Test Case ID: TC_API_011
    Role: admin
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'd9b88fd1-a755-42dd-99b5-8e659a710a5c'}/{EXECUTION_CONTEXT.get('step') or 'step_3365'}/approve"
    payload = None
    query = None

    response = safe_request(
        "POST",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_approve_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'd9b88fd1-a755-42dd-99b5-8e659a710a5c'}/{EXECUTION_CONTEXT.get('step') or 'step_3365'}/approve"
    response = safe_request("POST", url, headers=user_headers)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_approve_without_auth():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'd9b88fd1-a755-42dd-99b5-8e659a710a5c'}/{EXECUTION_CONTEXT.get('step') or 'step_3365'}/approve"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_approve_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'd9b88fd1-a755-42dd-99b5-8e659a710a5c'}/{EXECUTION_CONTEXT.get('step') or 'step_3365'}/approve"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_reject_as_admin(admin_headers):
    """
    Test Case ID: TC_API_016
    Role: admin
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'f5a30915-f6bf-4a3e-b32f-ce9cf6d74c8a'}/{EXECUTION_CONTEXT.get('step') or 'step_6143'}/reject"
    payload = None
    query = None

    response = safe_request(
        "POST",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_reject_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'f5a30915-f6bf-4a3e-b32f-ce9cf6d74c8a'}/{EXECUTION_CONTEXT.get('step') or 'step_6143'}/reject"
    response = safe_request("POST", url, headers=user_headers)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_reject_without_auth():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'f5a30915-f6bf-4a3e-b32f-ce9cf6d74c8a'}/{EXECUTION_CONTEXT.get('step') or 'step_6143'}/reject"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_steps_job_id_step_reject_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/{EXECUTION_CONTEXT.get('job_id') or 'f5a30915-f6bf-4a3e-b32f-ce9cf6d74c8a'}/{EXECUTION_CONTEXT.get('step') or 'step_6143'}/reject"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_admin_jobs_job_id_reset_as_admin(admin_headers):
    """
    Test Case ID: TC_API_021
    Role: admin
    Classification: create
    Risk Level: high
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '70915232-ffc8-4d66-989e-180d225dd69f'}/reset"
    payload = None
    query = None

    response = safe_request(
        "POST",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("POST", url, response)

    try:
        data = response.json()
        captured = LifecycleChainingEngine.extract_resource_values(data, {})
        EXECUTION_CONTEXT.register(captured)
    except Exception:
        pass

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_admin_jobs_job_id_reset_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '70915232-ffc8-4d66-989e-180d225dd69f'}/reset"
    response = safe_request("POST", url, headers=user_headers)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_admin_jobs_job_id_reset_without_auth():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '70915232-ffc8-4d66-989e-180d225dd69f'}/reset"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.high
def test_create_api_v1_api_workflows_workflows_admin_jobs_job_id_reset_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '70915232-ffc8-4d66-989e-180d225dd69f'}/reset"
    response = safe_request("POST", url)
    log_request_response("POST", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_v1_projects_projects_as_admin(admin_headers):
    """
    Test Case ID: TC_API_026
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_v1_projects_projects_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    response = safe_request("GET", url, headers=user_headers)
    log_request_response("GET", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.low
def test_get_api_v1_api_v1_projects_projects_without_auth():

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_v1_projects_projects_contract_stability():

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_health_health_as_admin(admin_headers):
    """
    Test Case ID: TC_API_031
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_health_health_as_user(user_headers):
    """
    Test Case ID: TC_API_032
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_health_health_contract_stability():

    url = f"{BASE_URL}/api/v1/api/health/health"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_status_as_admin(admin_headers):
    """
    Test Case ID: TC_API_035
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '1a4462a9-1e56-4dc3-98c5-5a1f9b9f69df'}/status"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_status_as_user(user_headers):
    """
    Test Case ID: TC_API_036
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '1a4462a9-1e56-4dc3-98c5-5a1f9b9f69df'}/status"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_status_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '1a4462a9-1e56-4dc3-98c5-5a1f9b9f69df'}/status"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_steps_step_as_admin(admin_headers):
    """
    Test Case ID: TC_API_039
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '3d2b2365-b8e2-4bc9-bd7d-2d123697e7b3'}/steps/{EXECUTION_CONTEXT.get('step') or 'step_8459'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_steps_step_as_user(user_headers):
    """
    Test Case ID: TC_API_040
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '3d2b2365-b8e2-4bc9-bd7d-2d123697e7b3'}/steps/{EXECUTION_CONTEXT.get('step') or 'step_8459'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_job_id_steps_step_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/{EXECUTION_CONTEXT.get('job_id') or '3d2b2365-b8e2-4bc9-bd7d-2d123697e7b3'}/steps/{EXECUTION_CONTEXT.get('step') or 'step_8459'}"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_dead_letter_as_admin(admin_headers):
    """
    Test Case ID: TC_API_043
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_dead_letter_as_user(user_headers):
    """
    Test Case ID: TC_API_044
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_dead_letter_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_jobs_job_id_as_admin(admin_headers):
    """
    Test Case ID: TC_API_047
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '2f7cb522-88c6-49f1-8e94-7226b3b834d6'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_jobs_job_id_as_user(user_headers):
    """
    Test Case ID: TC_API_048
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '2f7cb522-88c6-49f1-8e94-7226b3b834d6'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_admin_jobs_job_id_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/{EXECUTION_CONTEXT.get('job_id') or '2f7cb522-88c6-49f1-8e94-7226b3b834d6'}"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_events_job_id_as_admin(admin_headers):
    """
    Test Case ID: TC_API_051
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/{EXECUTION_CONTEXT.get('job_id') or 'b42023c8-7c4e-4f2f-ae76-1fd91190de07'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_events_job_id_as_user(user_headers):
    """
    Test Case ID: TC_API_052
    Role: user
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/{EXECUTION_CONTEXT.get('job_id') or 'b42023c8-7c4e-4f2f-ae76-1fd91190de07'}"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=user_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_events_job_id_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/{EXECUTION_CONTEXT.get('job_id') or 'b42023c8-7c4e-4f2f-ae76-1fd91190de07'}"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500

@pytest.mark.functional
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_jobs_as_admin(admin_headers):
    """
    Test Case ID: TC_API_055
    Role: admin
    Classification: read
    Risk Level: low
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    payload = None
    query = None

    response = safe_request(
        "GET",
        url,
        headers=admin_headers,
        json=payload if payload else None,
        params=query if query else None
    )

    log_request_response("GET", url, response)

    assert response.status_code in (200, 201, 202, 204)

@pytest.mark.security
@pytest.mark.rbac
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_jobs_as_user_forbidden(user_headers):

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    response = safe_request("GET", url, headers=user_headers)
    log_request_response("GET", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.security
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_jobs_without_auth():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code in (401, 403)

@pytest.mark.contract
@pytest.mark.low
def test_get_api_v1_api_workflows_workflows_jobs_contract_stability():

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    response = safe_request("GET", url)
    log_request_response("GET", url, response)

    assert response.status_code < 500
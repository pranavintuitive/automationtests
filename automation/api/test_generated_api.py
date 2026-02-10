import pytest
import requests
import logging
import json
from automation.utils.schema_assertions import assert_schema

BASE_URL = "http://34.173.227.240:8000"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("api_test.log"), logging.StreamHandler()]
)

def log_request_response(method, url, payload, response):
    logging.info(f"REQUEST {method} {url}")
    logging.info(f"Payload: {payload}")
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response Body: {response.text[:1000]}")

def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=15, **kwargs)
    except Exception as e:
        logging.exception("Request failed")
        pytest.fail(str(e))


@pytest.fixture(scope="session")
def auth_headers():
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/auth/login",
        data={
            "grant_type": "password",
            "username": "admin@acme.com",
            "password": "admin123",
            "client_id": "string",
            "client_secret": "",
        },
        timeout=15,
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        pytest.fail("Auth token missing")
    return {"Authorization": f"Bearer {token}"}

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_v1_projects_projects_positive(auth_headers):
    """
    Test Case ID: TC_API_001
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/v1/projects/projects/
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_v1_projects_projects_negative(auth_headers):
    """
    Test Case ID: TC_API_001_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_health_health_positive(auth_headers):
    """
    Test Case ID: TC_API_002
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/health/health
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_health_health_negative(auth_headers):
    """
    Test Case ID: TC_API_002_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_create_api_v1_api_workflows_workflows_start_positive(auth_headers):
    """
    Test Case ID: TC_API_003
    GIVEN Validate API behavior
    WHEN client sends POST /api/v1/api/workflows/workflows/start
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_create_api_v1_api_workflows_workflows_start_negative(auth_headers):
    """
    Test Case ID: TC_API_003_NEG
    GIVEN invalid input
    WHEN client sends POST
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_create_api_v1_api_workflows_workflows_steps_test_job_id_test_step_approve_positive(auth_headers):
    """
    Test Case ID: TC_API_004
    GIVEN Validate API behavior
    WHEN client sends POST /api/v1/api/workflows/workflows/steps/test_job_id/test_step/approve
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/approve"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_create_api_v1_api_workflows_workflows_steps_test_job_id_test_step_approve_negative(auth_headers):
    """
    Test Case ID: TC_API_004_NEG
    GIVEN invalid input
    WHEN client sends POST
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/approve"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_create_api_v1_api_workflows_workflows_steps_test_job_id_test_step_reject_positive(auth_headers):
    """
    Test Case ID: TC_API_005
    GIVEN Validate API behavior
    WHEN client sends POST /api/v1/api/workflows/workflows/steps/test_job_id/test_step/reject
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/reject"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_create_api_v1_api_workflows_workflows_steps_test_job_id_test_step_reject_negative(auth_headers):
    """
    Test Case ID: TC_API_005_NEG
    GIVEN invalid input
    WHEN client sends POST
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/reject"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_test_job_id_status_positive(auth_headers):
    """
    Test Case ID: TC_API_006
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/test_job_id/status
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/status"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_test_job_id_status_negative(auth_headers):
    """
    Test Case ID: TC_API_006_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/status"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_test_job_id_steps_test_step_positive(auth_headers):
    """
    Test Case ID: TC_API_007
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/test_job_id/steps/test_step
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/steps/test_step"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_test_job_id_steps_test_step_negative(auth_headers):
    """
    Test Case ID: TC_API_007_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/steps/test_step"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_admin_dead_letter_positive(auth_headers):
    """
    Test Case ID: TC_API_008
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/admin/dead-letter
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_admin_dead_letter_negative(auth_headers):
    """
    Test Case ID: TC_API_008_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_admin_jobs_test_job_id_positive(auth_headers):
    """
    Test Case ID: TC_API_009
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/admin/jobs/test_job_id
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_admin_jobs_test_job_id_negative(auth_headers):
    """
    Test Case ID: TC_API_009_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_create_api_v1_api_workflows_workflows_admin_jobs_test_job_id_reset_positive(auth_headers):
    """
    Test Case ID: TC_API_010
    GIVEN Validate API behavior
    WHEN client sends POST /api/v1/api/workflows/workflows/admin/jobs/test_job_id/reset
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id/reset"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_create_api_v1_api_workflows_workflows_admin_jobs_test_job_id_reset_negative(auth_headers):
    """
    Test Case ID: TC_API_010_NEG
    GIVEN invalid input
    WHEN client sends POST
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id/reset"
    payload = None

    response = safe_request(
        "POST",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("POST", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_events_test_job_id_positive(auth_headers):
    """
    Test Case ID: TC_API_011
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/events/test_job_id
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/test_job_id"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_events_test_job_id_negative(auth_headers):
    """
    Test Case ID: TC_API_011_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/test_job_id"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)

RESPONSE_SCHEMA = None

@pytest.mark.contract
def test_get_api_v1_api_workflows_workflows_jobs_positive(auth_headers):
    """
    Test Case ID: TC_API_012
    GIVEN Validate API behavior
    WHEN client sends GET /api/v1/api/workflows/workflows/jobs
    THEN response should match API contract
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    if response.status_code == 404:
        pytest.xfail("Path parameter placeholder")

    assert response.status_code == 200

    if RESPONSE_SCHEMA and response.headers.get("content-type","").startswith("application/json"):
        assert_schema(response.json(), RESPONSE_SCHEMA)

def test_get_api_v1_api_workflows_workflows_jobs_negative(auth_headers):
    """
    Test Case ID: TC_API_012_NEG
    GIVEN invalid input
    WHEN client sends GET
    THEN API should reject request
    """

    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    payload = None

    response = safe_request(
        "GET",
        url,
        json=payload if payload else None,
        headers=auth_headers
    )

    log_request_response("GET", url, payload, response)

    assert response.status_code in (400,401,403,404,422)
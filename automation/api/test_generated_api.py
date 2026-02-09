import pytest
import requests
import logging
import json

BASE_URL = "http://34.135.61.167:8000"

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_test.log"),
        logging.StreamHandler()
    ]
)

def log_request_response(method, url, payload, response):
    logging.info(f"REQUEST {method} {url}")
    logging.info(f"Payload: {payload}")
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response Body: {response.text[:1000]}")

# ----------------------------
# Safe request wrapper
# ----------------------------
def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=15, **kwargs)
    except Exception as e:
        logging.exception(f"Request failed: {method} {url}")
        pytest.fail(str(e))


# ----------------------------
# AUTH FIXTURE
# ----------------------------
@pytest.fixture(scope="session")
def auth_headers():
    try:
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
            pytest.fail("Auth token missing in login response")

        return {
            "Authorization": f"Bearer {token}"
        }
    except Exception as e:
        pytest.fail(f"Authentication failed: {e}")



def test_api_v1_auth_auth_login_post_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/auth/auth/login"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("POST", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code < 400

def test_api_v1_auth_auth_login_post_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/auth/auth/login"
    payload = None

    if payload:
        response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_v1_projects_projects_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_v1_projects_projects_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/v1/projects/projects/"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_health_health_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_health_health_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/health/health"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_start_post_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("POST", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_start_post_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/start"
    payload = None

    if payload:
        response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_steps_test_job_id_test_step_approve_post_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/approve"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("POST", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_steps_test_job_id_test_step_approve_post_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/approve"
    payload = None

    if payload:
        response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_steps_test_job_id_test_step_reject_post_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/reject"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("POST", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_steps_test_job_id_test_step_reject_post_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/steps/test_job_id/test_step/reject"
    payload = None

    if payload:
        response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_test_job_id_status_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/status"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_test_job_id_status_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/status"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_test_job_id_steps_test_step_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/steps/test_step"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_test_job_id_steps_test_step_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/test_job_id/steps/test_step"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_admin_dead_letter_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_admin_dead_letter_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/dead-letter"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_admin_jobs_test_job_id_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_admin_jobs_test_job_id_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_admin_jobs_test_job_id_reset_post_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id/reset"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("POST", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_admin_jobs_test_job_id_reset_post_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/admin/jobs/test_job_id/reset"
    payload = None

    if payload:
        response = safe_request("POST", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("POST", url, headers=auth_headers)

    log_request_response("POST", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_events_test_job_id_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/test_job_id"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_events_test_job_id_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/events/test_job_id"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)

def test_api_v1_api_workflows_workflows_jobs_get_positive(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    payload = None

    if payload:
        if "None" == "form":
            response = safe_request("GET", url, data=payload, headers=auth_headers)
        else:
            response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code < 400

def test_api_v1_api_workflows_workflows_jobs_get_negative(auth_headers):
    url = f"{BASE_URL}/api/v1/api/workflows/workflows/jobs"
    payload = None

    if payload:
        response = safe_request("GET", url, json=payload, headers=auth_headers)
    else:
        response = safe_request("GET", url, headers=auth_headers)

    log_request_response("GET", url, payload, response)
    assert response.status_code in (400, 401, 403, 404, 422)
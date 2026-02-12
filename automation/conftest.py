import os
import pytest
import requests


BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise RuntimeError("BASE_URL environment variable is not configured")

@pytest.fixture(scope="session")
def admin_headers():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip("Admin credentials not configured")
    token = authenticate(username, password)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def user_headers():
    username = os.getenv("USER_USERNAME")
    password = os.getenv("USER_PASSWORD")
    if not username or not password:
        pytest.skip("User credentials not configured")
    token = authenticate(username, password)
    return {"Authorization": f"Bearer {token}"}

def authenticate(username: str, password: str) -> str:
    login_url = f"{BASE_URL}/api/v1/auth/auth/login"

    form_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "string",
        "client_secret": "",
    }

    response = requests.post(
        login_url,
        data=form_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        timeout=15,
    )

    response.raise_for_status()

    token = response.json().get("access_token")
    if not token:
        raise RuntimeError("Authentication failed: access_token missing")

    return token

import os
import pytest
import requests

BASE_URL = os.getenv("BASE_URL")

def login(username: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/auth/login",
        data={
            "grant_type": os.getenv("GRANT_TYPE", "password"),
            "username": username,
            "password": password,
            "scope": os.getenv("SCOPE", ""),
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        timeout=15,
    )

    response.raise_for_status()
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def admin_headers():
    token = login(
        os.getenv("ADMIN_USERNAME"),
        os.getenv("ADMIN_PASSWORD"),
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def user_headers():
    token = login(
        os.getenv("USER_USERNAME"),
        os.getenv("USER_PASSWORD"),
    )
    return {"Authorization": f"Bearer {token}"}
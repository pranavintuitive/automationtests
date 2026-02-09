import pytest
import requests

BASE_URL = "http://34.135.61.167:8000/api/v1"

def test_oauth2_password_login():
    url = f"{BASE_URL}/auth/auth/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    form_data = {
        "grant_type": "password",
        "username": "admin@acme.com",
        "password": "admin123",
        "scope": "",
        "client_id": "string",
        "client_secret": ""
    }
    response = requests.post(url, data=form_data, headers=headers)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert isinstance(json_response["access_token"], str)
    assert len(json_response["access_token"]) > 0
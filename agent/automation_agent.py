import os
import json
from pathlib import Path

import requests
from openai import OpenAI
from agent.behavior_explorer import BehaviorExplorer
from agent.intent_model_builder import IntentModelBuilder
from agent.swagger_reader import read_swagger, extract_endpoints
from agent.test_generator import generate_tests

client = OpenAI()

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = ROOT / "automation"
UI_DIR = AUTOMATION_DIR / "ui"
API_DIR = AUTOMATION_DIR / "api"
UTILS_DIR = AUTOMATION_DIR / "utils"
PIPELINE_FILE = ROOT / ".github/workflows/automation.yml"


# ---------------------------
# Utilities
# ---------------------------
def safe_write(path: Path, content: str):
    if path.exists():
        print(f"{path} already exists- overriding")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[CREATED] {path}")

    path.write_text(content, encoding="utf-8")
    print(f"[updated] {path}")


def llm_generate(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate ONLY runnable code. No explanations.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# ---------------------------
# UI Test Generator
# ---------------------------
def generate_ui_test(base_url: str, flow: str):
    prompt = f"""
Generate Playwright Python test using pytest.

Rules:
- No explanations
- No markdown
- Use sync_playwright
- Deterministic waits
- Base URL: {base_url}

Test flow:
{flow}
"""
    code = llm_generate(prompt)
    clean_code = strip_markdown_fences(code)
    safe_write(UI_DIR / f"test_{flow}_ui.py", clean_code)


# ---------------------------
# API Test Generator
# ---------------------------
def generate_api_test(base_url: str, endpoints: list):
    prompt = f"""
Generate pytest API tests using requests.

STRICT RULES:
- Output ONLY raw Python code
- NO markdown
- Base URL: {base_url}
- If auth_type is oauth2_password:
  - Use requests.post(..., data=form_data)
  - Use Content-Type application/x-www-form-urlencoded
- Validate status code and access_token in response

Endpoint definition:
{json.dumps(endpoints, indent=2)}
"""

    code = llm_generate(prompt)
    clean_code = strip_markdown_fences(code)
    safe_write(API_DIR / "test_api.py", clean_code)


# ---------------------------
# Common Files
# ---------------------------
def ensure_common_files(base_url: str):
    safe_write(UTILS_DIR / "config.py", f'BASE_URL = "{base_url}"\n')
    
    safe_write(
        AUTOMATION_DIR / "requirements.txt",
        """pytest
pytest-html
requests
playwright
python-dotenv
""",
    )



# ---------------------------
# GitHub Actions Pipeline
# ---------------------------
def ensure_pipeline():
    if not PIPELINE_FILE.exists():
        PIPELINE_FILE.parent.mkdir(parents=True, exist_ok=True)

    PIPELINE_FILE.write_text(
        """name: Automation Tests

on:
  push:
  workflow_dispatch:

jobs:
  automation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r automation/requirements.txt
          playwright install --with-deps

      - name: Set environment variables
        run: |
            echo "BASE_URL=${{ secrets.BASE_URL }}" >> $GITHUB_ENV
            echo "ADMIN_USERNAME=${{ secrets.ADMIN_USERNAME }}" >> $GITHUB_ENV
            echo "ADMIN_PASSWORD=${{ secrets.ADMIN_PASSWORD }}" >> $GITHUB_ENV
            echo "USER_USERNAME=${{ secrets.USER_USERNAME }}" >> $GITHUB_ENV
            echo "USER_PASSWORD=${{ secrets.USER_PASSWORD }}" >> $GITHUB_ENV
            echo "CLIENT_ID=${{ secrets.CLIENT_ID }}" >> $GITHUB_ENV
            echo "CLIENT_SECRET=${{ secrets.CLIENT_SECRET }}" >> $GITHUB_ENV
      
      - name: Run tests
        run: |
          pytest automation --html=report.html --self-contained-html || true

      - name: Publish report
        uses: actions/upload-artifact@v4
        with:
          name: automation-report
          path: report.html
""",
        encoding="utf-8",
    )
    print("[CREATED] GitHub Actions pipeline")

def ensure_fixtures():
    """
    Always generates authentication fixtures.
    Overwrites existing conftest.py to guarantee consistency.
    """

    conftest_path = AUTOMATION_DIR / "conftest.py"
    conftest_path.parent.mkdir(parents=True, exist_ok=True)

    conftest_path.write_text(
        """
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
""".strip(),
        encoding="utf-8",
    )

    print("[UPDATED] conftest.py with dynamic auth fixtures")


# ---------------------------
# Main Agent Entry
# ---------------------------


def run_agent(spec: dict):

    swagger_url = spec.get("swagger_url")
    base_url = spec.get("base_url")
    environment = spec.get("environment", "staging")

    if not swagger_url:
        raise ValueError("swagger_url is required for API test generation")

    # ----------------------------
    #  Read Swagger
    # ----------------------------
    print("Reading Swagger...")
    swagger_spec = read_swagger(swagger_url)
    swagger_base_url, endpoints = extract_endpoints(swagger_spec)

    base_url = swagger_base_url or base_url

    print(f"Discovered {len(endpoints)} endpoints")

    # ----------------------------
    # Role Authentication
    # ----------------------------
    print("Authenticating roles...")

    role_headers = {}
    for role_name, credentials in spec.get("roles", {}).items():
        
        headers = authenticate_role(
            base_url,
            spec["auth"],
            credentials
        )
        role_headers[role_name] = headers

    print(f"Authenticated roles: {list(role_headers.keys())}")

   # ----------------------------
    # Behavior Explorer
    # ----------------------------
    print("Running Behavior Explorer...")

    explorer = BehaviorExplorer(
        base_url=base_url,
        endpoints=endpoints,
        role_headers=role_headers,   # <-- multi-role support
        environment=environment,
    )

    behavior_report = explorer.explore_all()

    print(f"Behavior analysis completed for {len(behavior_report)} endpoints")


    # ----------------------------
    # Intent Model Builder
    # ----------------------------
    print("Building Intent Model...")

    builder = IntentModelBuilder(behavior_report)
    intent_model = builder.build()
    builder.save("intent_model.json")

    print("Intent model saved")

    # ----------------------------
    # Generate Tests
    # ----------------------------
    if spec.get("generate_api_tests", True):
        generate_tests(base_url, intent_model, swagger_spec)

    if not spec.get("enable_ui_tests", False):
        print("UI tests are disabled (code retained, not executed)")

    # Ensure CI setup
    ensure_common_files(base_url)
    ensure_pipeline()
    ensure_fixtures()
    print("\nAutomation agent completed successfully")



def strip_markdown_fences(code: str) -> str:
    code = code.strip()

    # Remove triple-backtick fences
    if code.startswith("```"):
        code = code.split("```", 1)[1]

    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]

    code = code.strip()

    # Remove a leading language tag like "python"
    first_line = code.splitlines()[0].strip().lower()
    if first_line in {"python", "py"}:
        code = "\n".join(code.splitlines()[1:])

    return code.strip()


def authenticate_role(base_url: str, auth_config: dict, credentials: dict) -> dict:
    """
    Authenticates a role using OAuth2 password flow.
    Returns headers with Bearer token.
    """

    login_url = f"{base_url.rstrip('/')}{auth_config['login_path']}"

    form_data = {
        "grant_type": auth_config.get("grant_type", "password"),
        "username": credentials["username"],
        "password": credentials["password"],
        "scope": "",
        "client_id": auth_config.get("client_id", "string"),
        "client_secret": auth_config.get("client_secret", ""),
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
        raise ValueError("Authentication succeeded but access_token missing")

    return {
        "Authorization": f"Bearer {token}"
    }


# ---------------------------
# Run directly
# ---------------------------
if __name__ == "__main__":

    SPEC = {
        # Swagger / OpenAPI URL (JSON)
        "swagger_url": "http://34.56.161.228:8000/openapi.json",
        # Base URL fallback (used if swagger has no servers section)
        "base_url": "http://34.56.161.228:8000",
        "environment": "staging",
        "roles": {
                "admin": {
                            "username": "admin@acme.com",
                            "password": "admin123"
                        },
                "user": {
                        "username": "user@acme.com",
                        "password": "user123"
                        }
            },
            "auth": {
                        "login_path": "/api/v1/auth/auth/login",
                        "grant_type": "password",
                        "client_id": "string",
                        "client_secret": ""
                    },
        # Keep UI code in repo, but do not run it
        "enable_ui_tests": False,
        # API test generation options
        "generate_api_tests": True,
        # Overwrite previously generated API tests
        "overwrite": True,
    }


    run_agent(SPEC)
import os
import json
from pathlib import Path
from openai import OpenAI
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
def ensure_common_files():
    safe_write(UTILS_DIR / "config.py", """BASE_URL = """ "")

    safe_write(
        AUTOMATION_DIR / "requirements.txt",
        """pytest
pytest-html
requests
playwright
""",
    )

    safe_write(AUTOMATION_DIR / "conftest.py", """import pytest""")


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

      - name: Run tests
        run: |
          pytest automation --html=report.html --self-contained-html

      - name: Publish report
        uses: actions/upload-artifact@v4
        with:
          name: automation-report
          path: report.html
""",
        encoding="utf-8",
    )
    print("[CREATED] GitHub Actions pipeline")


# ---------------------------
# Main Agent Entry
# ---------------------------


def run_agent(spec: dict):

    # --- Swagger driven API discovery ---
    swagger_url = spec.get("swagger_url")
    base_url = spec.get("base_url")

    if swagger_url:
        swagger_spec = read_swagger(swagger_url)
        swagger_base_url, endpoints = extract_endpoints(swagger_spec)

        # Swagger server URL takes precedence
        base_url = swagger_base_url or base_url
    else:
        raise ValueError("swagger_url is required for API test generation")

    # --- Generate API tests ---
    if spec.get("generate_api_tests", True):
        generate_tests(base_url, endpoints)

    # --- UI tests intentionally NOT executed ---
    if not spec.get("enable_ui_tests", False):
        print("ℹ️ UI tests are disabled (code retained, not executed)")

    print("\n✅ Automation agent completed successfully")


# def run_agent(spec: dict):
#     base_url = spec["base_url"]

#     ensure_common_files()
#     ensure_pipeline()

#     for flow in spec.get("ui_flows", []):
#         generate_ui_test(base_url, flow)

#     generate_api_test(spec["api_url"], spec.get("api_endpoints", []))

#     print("\n✅ Automation agent completed successfully")


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


# ---------------------------
# Run directly
# ---------------------------
if __name__ == "__main__":

    SPEC = {
        # Swagger / OpenAPI URL (JSON)
        "swagger_url": "http://34.135.61.167:8000/openapi.json",
        # Base URL fallback (used if swagger has no servers section)
        "base_url": "http://34.135.61.167:8000",
        # Keep UI code in repo, but do not run it
        "enable_ui_tests": False,
        # API test generation options
        "generate_api_tests": True,
        # Overwrite previously generated API tests
        "overwrite": True,
    }

    run_agent(SPEC)

# if __name__ == "__main__":
#     SPEC = {
#         "base_url": "http://34.135.61.167:8000/",
#         "api_url": "http://34.135.61.167:8000/api/v1",
#         "ui_flows": ["login"],
#         "api_endpoints": [
#             {
#                 "method": "POST",
#                 "path": "/auth/auth/login",
#                 "auth_type": "oauth2_password",
#                 "form_data": {
#                     "grant_type": "password",
#                     "username": "admin@acme.com",
#                     "password": "admin123",
#                     "scope": "",
#                     "client_id": "string",
#                     "client_secret": "",
#                 },
#             }
#         ],
#     }

#     run_agent(SPEC)
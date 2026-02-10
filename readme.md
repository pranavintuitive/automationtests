# Automation Test Agent (Swagger-Driven)

An intelligent automation agent that **reads Swagger/OpenAPI specifications** and **generates deterministic, maintainable API tests** with logging, reporting, and CI/CD support.

The agent focuses on **contract validation, functional behavior, and negative scenarios**, while ensuring:
- deterministic test data
- repeatable executions
- non-destructive behavior across environments
- always-published test reports (even on failures)

---

##  Key Capabilities

### Swagger-Driven Test Generation
- Reads OpenAPI / Swagger definitions
- Extracts endpoints, methods, parameters, schemas
- Automatically generates:
  - Positive tests
  - Negative tests
  - Authentication-aware tests

###  Deterministic Test Data
- All payloads are generated using a **deterministic data factory**
- No randomness → no flaky tests
- Same Swagger + same inputs = same tests every run

###  Contract (Schema) Validation
- Response bodies are validated against Swagger response schemas
- Detects:
  - missing fields
  - type mismatches
  - contract regressions

###  BDD-Style Readable Tests
Generated tests follow a **Given / When / Then** structure:

###  prerequisits
    -python 3.12.x
    -sudo apt install python3-pip
    -pip install --upgrade pip
    -pip install openai python-dotenv
```python
"""
Test Case ID: TC_API_001
GIVEN a valid request to fetch projects
WHEN the client sends a GET request
THEN the API should return a successful response
"""
```
# Project Structure
  
    automationtestagent/
    ├── agent/                       
    │   ├── automation_agent.py
    │   ├── swagger_reader.py
    │   ├── test_generator.py
    │   ├── generate_tests.py
    │   └── data_factory.py
    │
    ├── automation/                  
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── test_api.py
    │   │   └── test_generated_api.py
    │   ├── utils/
    │   │   ├── config.py
    │   │   └── schema_assertions.py
    │   ├── ui/
    │   │   └── test_login_ui.py
    │   └── conftest.py
    │
    ├── helpers/
    │   └── outputcleaner.py
    │
    ├── pytest.ini
    ├── requirements.txt
    └── README.md


# Instalation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Agent
python -m agent.automation_agent

# Run Locally
pytest automation --html=report.html --self-contained-html

# Selective Test Execution
## Contract
pytest -m contract
## Functional
pytest -m functional

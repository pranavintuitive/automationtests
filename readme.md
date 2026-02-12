# Automation Test Agent  
## Swagger-Driven, Behavior-Aware, Deterministic Test Generation Framework

---

## What This Project Is

Automation Test Agent is an intelligent API automation framework that:

- Reads OpenAPI / Swagger specifications
- Explores live runtime behavior
- Detects authentication and role access
- Builds a structured intent model
- Generates deterministic, schema-compliant test payloads
- Produces production-ready pytest test suites
- Generates CI/CD pipelines automatically

This is not a simple test generator.

It is a layered automation architecture designed to evolve toward:
- Stateful lifecycle testing
- Dependency resolution
- Intelligent chaining
- Contract drift detection
- Risk-based coverage modeling

---

# Architectural Vision

The framework follows a strict layered design:

Swagger → Behavior Explorer → Intent Model →
Test Data Resolution Engine → Test Generator → Pytest Suite → CI Pipeline


Each layer has a clearly defined responsibility and does not overlap concerns.

---

# Core Architectural Layers

---

## 1. Swagger Reader (Structural Layer)

**File:** `agent/swagger_reader.py`

Responsibilities:
- Load OpenAPI JSON
- Extract endpoints
- Extract request/response schemas
- Provide structural metadata

This layer understands the system contract — not behavior.

---

## 2. Behavior Explorer (Runtime Discovery Layer)

**File:** `agent/behavior_explorer.py`

Responsibilities:
- Call live endpoints
- Detect authentication requirements
- Classify role-based access
- Detect pagination, filtering, sorting
- Identify async behavior
- Capture runtime response schema

Important logic:
- 401 and 403 → authorization failure
- 422 → validation failure (access allowed)

This prevents misclassifying POST endpoints as forbidden.

Output: Behavior report.

---

## 3. Intent Model Builder (Business Interpretation Layer)

**File:** `agent/intent_model_builder.py`

Converts behavior into a business-aligned intent model.

Each endpoint is classified into:
- create
- read
- update
- delete
- search

Each endpoint gets:
- risk level
- test types (contract / functional / security)
- role access mapping

Output file:
intent_model.json

Intent model contains business testing intent — not raw Swagger.

---

## 4. Test Data Resolution Engine (Intelligence Layer)

**Directory:** `resolution/`

This is the most critical component.

Responsibilities:

### Schema Handling
- Recursive `$ref` resolution
- Nested DTO expansion
- `anyOf` normalization
- Nullable handling

### Format Awareness
- `format: uuid` → deterministic UUID generation
- `format: date-time` → ISO timestamps
- Primitive type handling

### Deterministic Data
- No randomness
- Reproducible payloads
- Stable test generation

### Object Construction
Generates payloads matching Swagger exactly, including nested structures:

Example:
  ```json
  {
    "product_idea": "string",
    "target_audience": {
      "primary": ["string"],
      "secondary": ["string"]
    },
    "job_id": "uuid"
  }
  "target_audience": "string" ```


  repo/
    ├── agent/
    │   ├── automation_agent.py
    │   ├── behavior_explorer.py
    │   ├── intent_model_builder.py
    │   ├── swagger_reader.py
    │   ├── test_generator.py
    │   └── data_factory.py
    │
    ├── resolution/
    │   ├── engine.py
    │   ├── schema_analyzer.py
    │   ├── field_resolver.py
    │   ├── dependency_resolver.py
    │   ├── strategy_selector.py
    │   ├── validator.py
    │   └── ...
    │
    ├── automation/
    ├── intent_model.json
    ├── pytest.ini
    ├── requirements.txt
    └── README.md

"""
Deterministic Data Factory
--------------------------
Generates repeatable, non-random test data
based on test case ID, field name, and type.

Guarantees:
- Same test case → same data every run
- No flaky behavior
- CI reproducibility
"""

import hashlib


def _stable_hash(value: str) -> int:
    return int(hashlib.sha256(value.encode()).hexdigest(), 16)


def deterministic_value(tc_id: str, field: str, type_name: str):
    seed = f"{tc_id}:{field}"
    h = _stable_hash(seed)

    if type_name == "string":
        return f"{field}_{h % 10000}"

    if type_name == "integer":
        return h % 100

    if type_name == "number":
        return round((h % 1000) / 10, 2)

    if type_name == "boolean":
        return True

    if type_name == "array":
        return []

    if type_name == "object":
        return {}

    return None

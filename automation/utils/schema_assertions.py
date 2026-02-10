"""
Contract Schema Assertions
--------------------------
Generated from Swagger/OpenAPI schemas.
"""

def assert_schema(data, schema, path="response"):
    if schema is None:
        return

    schema_type = schema.get("type")

    if schema_type == "object":
        assert isinstance(data, dict), f"{path} should be an object"

        required = schema.get("required", [])
        properties = schema.get("properties", {})

        for field in required:
            assert field in data, f"{path}.{field} is required but missing"

        for field, field_schema in properties.items():
            if field in data:
                assert_schema(
                    data[field],
                    field_schema,
                    f"{path}.{field}"
                )

    elif schema_type == "array":
        assert isinstance(data, list), f"{path} should be an array"
        item_schema = schema.get("items")
        if item_schema and data:
            assert_schema(data[0], item_schema, f"{path}[0]")

    elif schema_type == "string":
        assert isinstance(data, str), f"{path} should be string"

    elif schema_type == "integer":
        assert isinstance(data, int), f"{path} should be integer"

    elif schema_type == "number":
        assert isinstance(data, (int, float)), f"{path} should be number"

    elif schema_type == "boolean":
        assert isinstance(data, bool), f"{path} should be boolean"
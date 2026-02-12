class LifecycleContext:
    """
    Holds runtime-created resource identifiers
    """
    def __init__(self):
        self.resources = {}

    def register(self, key: str, value: str):
        self.resources[key] = value

    def get(self, key: str):
        return self.resources.get(key)


class LifecycleChainingEngine:

    @staticmethod
    def extract_resource_values(response_json: dict, swagger_spec: dict) -> dict:
        if not isinstance(response_json, dict):
            return {}

        path_param_schemas = []

        paths = swagger_spec.get("paths", {})

        for path, methods in paths.items():
            for method_data in methods.values():
                for param in method_data.get("parameters", []):
                    if param.get("in") == "path":
                        path_param_schemas.append(param.get("schema", {}))

        resources = {}

        for key, value in response_json.items():
            if not isinstance(value, (str, int)):
                continue

            for schema in path_param_schemas:
                if LifecycleChainingEngine.matches_schema(
                    value,
                    schema.get("type"),
                    schema.get("format")
                ):
                    resources[key] = value

        return resources

    @staticmethod
    def matches_schema(value, expected_type, expected_format):

        if expected_type == "string":
            if expected_format == "uuid":
                import re
                return isinstance(value, str) and re.match(
                    r"^[0-9a-fA-F-]{36}$", value
                )

            return isinstance(value, str)

        if expected_type == "integer":
            return isinstance(value, int)

        return False

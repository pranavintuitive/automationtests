# agent/resolution/schema_analyzer.py

from typing import Dict, Any
from .context import StepResolutionContext


class SchemaAnalyzer:
    """
    Extracts request schema information from OpenAPI spec.
    """

    def analyze(self, context: StepResolutionContext) -> StepResolutionContext:
        paths = context.swagger_spec.get("paths", {})
        endpoint_spec = paths.get(context.endpoint, {})
        method_spec = endpoint_spec.get(context.http_method.lower(), {})

        request_body = method_spec.get("requestBody", {})
        content = request_body.get("content", {})
        json_schema = content.get("application/json", {}).get("schema", {})

        # Resolve $ref if present
        if "$ref" in json_schema:
            ref_path = json_schema["$ref"]
            json_schema = self._resolve_ref(ref_path, context.swagger_spec)

        context.request_schema = self._resolve_nested_refs(json_schema, context.swagger_spec)
        context.required_fields = json_schema.get("required", [])

        parameters = method_spec.get("parameters", [])

        for param in parameters:
            name = param.get("name")
            location = param.get("in")
            schema = param.get("schema", {})

            if location == "path":
                context.path_params_schema[name] = schema
            elif location == "query":
                context.query_params_schema[name] = schema

        return context


    def _resolve_ref(self, ref_path: str, swagger_spec: dict):
        """
        Resolves local $ref like #/components/schemas/XYZ
        """
        parts = ref_path.strip("#/").split("/")
        node = swagger_spec
        for part in parts:
            node = node.get(part, {})
        return node

    def _resolve_nested_refs(self, schema: dict, swagger_spec: dict):
        """
        Recursively resolve $ref inside schema.
        """

        if not isinstance(schema, dict):
            return schema

        # Resolve direct $ref
        if "$ref" in schema:
            resolved = self._resolve_ref(schema["$ref"], swagger_spec)
            return self._resolve_nested_refs(resolved, swagger_spec)

        # Resolve anyOf
        if "anyOf" in schema:
            return {
                "anyOf": [
                    self._resolve_nested_refs(option, swagger_spec)
                    for option in schema["anyOf"]
                ]
            }

        # Resolve properties recursively
        if "properties" in schema:
            return {
                **schema,
                "properties": {
                    key: self._resolve_nested_refs(value, swagger_spec)
                    for key, value in schema["properties"].items()
                },
            }

        # Resolve array items
        if "items" in schema:
            return {
                **schema,
                "items": self._resolve_nested_refs(schema["items"], swagger_spec),
            }

        return schema

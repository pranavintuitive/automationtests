# resolution/field_resolver.py

from typing import Any, Dict
from .context import StepResolutionContext
from agent.data_factory import deterministic_value
import uuid
from datetime import datetime
class FieldResolver:
    """
    Builds resolved request payload using strategy map.
    """

    def resolve(self, context: StepResolutionContext) -> StepResolutionContext:
        properties = context.request_schema.get("properties", {})

        resolved_body: Dict[str, Any] = {}

        tc_id = f"TC_{context.deterministic_seed or 1:03d}"

        for field_name, schema in properties.items():
            strategy = context.strategy_map.get(field_name, "DEFAULT")

            if strategy == "INTENT_OVERRIDE":
                resolved_body[field_name] = context.intent_metadata.get(field_name)

            elif strategy == "REUSE":
                resolved_body[field_name] = context.dependency_map[field_name]["value"]

            elif strategy == "ENUM_PICK":
                enum_values = schema.get("enum", [])
                resolved_body[field_name] = enum_values[0] if enum_values else None

            else:
                resolved_body[field_name] = self._generate_value(
                    schema,
                    tc_id,
                    field_name
                )

        context.resolved_body = resolved_body

        # Resolve path params
        for param_name, dependency in context.dependency_map.items():
            if param_name in context.path_params_schema:
                if dependency["source"] == "execution_context":
                    context.resolved_path_params[param_name] = dependency["value"]
                else:
                    context.resolved_path_params[param_name] = deterministic_value(
                        tc_id,
                        param_name,
                        context.path_params_schema[param_name].get("type", "string")
                    )

        return context

    def _generate_value(self, schema: Dict[str, Any], tc_id: str, field_name: str) -> Any:

        # -------------------------
        # Normalize anyOf
        # -------------------------
        if "anyOf" in schema:
            for option in schema["anyOf"]:
                if option.get("type") != "null":
                    schema = option
                    break

        schema_type = schema.get("type", "string")
        schema_format = schema.get("format")

        # -------------------------
        # Format-aware generation
        # -------------------------
        if schema_format == "uuid":
            namespace = uuid.NAMESPACE_DNS
            return str(uuid.uuid5(namespace, f"{tc_id}-{field_name}"))

        if schema_format == "date-time":
            return datetime.utcnow().isoformat()

        # -------------------------
        # Object
        # -------------------------
        if schema_type == "object":
            properties = schema.get("properties", {})
            return {
                key: self._generate_value(value_schema, tc_id, key)
                for key, value_schema in properties.items()
            }

        # -------------------------
        # Array
        # -------------------------
        if schema_type == "array":
            item_schema = schema.get("items", {})
            return [self._generate_value(item_schema, tc_id, field_name)]

        # -------------------------
        # Default primitive
        # -------------------------
        return deterministic_value(tc_id, field_name, schema_type)

# agent/resolution/validator.py

from .context import StepResolutionContext


class SchemaValidator:
    """
    Validates resolved payload against required schema constraints.
    """

    def validate(self, context: StepResolutionContext) -> StepResolutionContext:
        required_fields = context.required_fields or []

        for field in required_fields:
            if field not in context.resolved_body:
                raise ValueError(f"Missing required field: {field}")

        # Enum validation
        properties = context.request_schema.get("properties", {})

        for field_name, schema in properties.items():
            if "enum" in schema:
                allowed = schema["enum"]
                value = context.resolved_body.get(field_name)
                if value not in allowed:
                    raise ValueError(
                        f"Invalid enum value for {field_name}: {value}"
                    )

        return context

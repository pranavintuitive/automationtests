# agent/resolution/strategy_selector.py

from .context import StepResolutionContext


class DataStrategySelector:
    """
    Selects strategy for resolving each field.
    """

    def select(self, context: StepResolutionContext) -> StepResolutionContext:
        intent = context.intent_metadata or {}

        properties = context.request_schema.get("properties", {})

        for field_name, schema in properties.items():

            # Priority 1: Explicit intent override
            if field_name in intent:
                context.strategy_map[field_name] = "INTENT_OVERRIDE"
                continue

            # Priority 2: Execution context reuse
            dependency = context.dependency_map.get(field_name)
            if dependency and dependency.get("source") == "execution_context":
                context.strategy_map[field_name] = "REUSE"
                continue

            # Priority 3: Enum field
            if "enum" in schema:
                context.strategy_map[field_name] = "ENUM_PICK"
                continue

            # Priority 4: Required field
            if field_name in context.required_fields:
                context.strategy_map[field_name] = "GENERATE"
                continue

            # Default
            context.strategy_map[field_name] = "DEFAULT"

        return context

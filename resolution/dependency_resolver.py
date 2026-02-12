# agent/resolution/dependency_resolver.py

from typing import Any
from .context import StepResolutionContext


class DependencyResolver:
    """
    Resolves dependencies like path params and entity references
    from execution context.
    """

    def resolve(self, context: StepResolutionContext) -> StepResolutionContext:
        execution_memory = context.execution_context or {}

        # Resolve path parameters
        for param_name in context.path_params_schema.keys():
            if param_name in execution_memory:
                context.dependency_map[param_name] = {
                    "source": "execution_context",
                    "value": execution_memory[param_name],
                }
            else:
                context.dependency_map[param_name] = {
                    "source": "generate",
                    "value": None,
                }

        # Resolve body-level dependencies
        properties = context.request_schema.get("properties", {})

        for field_name in properties.keys():
            if field_name in execution_memory:
                context.dependency_map[field_name] = {
                    "source": "execution_context",
                    "value": execution_memory[field_name],
                }
            else:
                if field_name not in context.dependency_map:
                    context.dependency_map[field_name] = {
                        "source": "generate",
                        "value": None,
                    }

        return context

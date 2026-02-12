# agent/resolution/rbac_injector.py

from .context import StepResolutionContext


class RBACInjector:
    """
    Injects role-based headers and applies field-level restrictions if required.
    """

    def inject(self, context: StepResolutionContext) -> StepResolutionContext:
        role = context.role_context.get("role")
        token = context.role_context.get("token")

        if token:
            context.resolved_headers["Authorization"] = f"Bearer {token}"

        # Optional: enforce role-based restrictions
        restricted_fields = context.role_context.get("restricted_fields", [])

        for field in restricted_fields:
            if field in context.resolved_body:
                context.resolved_body.pop(field)

        return context

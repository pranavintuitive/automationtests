# agent/resolution/engine.py

from .contracts import (
    TestStepResolutionRequest,
    ResolvedExecutionRequest,
)
from .context import StepResolutionContext
from .schema_analyzer import SchemaAnalyzer
from .dependency_resolver import DependencyResolver
from .strategy_selector import DataStrategySelector
from .deterministic_binder import DeterministicBinder
from .field_resolver import FieldResolver
from .rbac_injector import RBACInjector
from .validator import SchemaValidator


class TestDataResolutionEngine:
    """
    Orchestrates full resolution pipeline.
    """

    def __init__(self):
        self.schema_analyzer = SchemaAnalyzer()
        self.dependency_resolver = DependencyResolver()
        self.strategy_selector = DataStrategySelector()
        self.deterministic_binder = DeterministicBinder()
        self.field_resolver = FieldResolver()
        self.rbac_injector = RBACInjector()
        self.validator = SchemaValidator()

    def resolve(
        self, request: TestStepResolutionRequest
    ) -> ResolvedExecutionRequest:

        context = StepResolutionContext(
            endpoint=request.endpoint,
            http_method=request.http_method,
            swagger_spec=request.swagger_spec,
            intent_metadata=request.intent_metadata,
            role_context=request.role_context,
            execution_context=request.execution_context,
            deterministic_seed=request.deterministic_seed,
            request_content_type= request.request_content_type,
        )

        # Pipeline
        context = self.schema_analyzer.analyze(context)
        context = self.dependency_resolver.resolve(context)
        context = self.strategy_selector.select(context)
        context = self.deterministic_binder.bind(context)
        context = self.field_resolver.resolve(context)
        context = self.rbac_injector.inject(context)
        context = self.validator.validate(context)
        print(f"request_content_type: {context.request_content_type}")
        return ResolvedExecutionRequest(
            url=context.endpoint,
            http_method=context.http_method,
            path_params=context.resolved_path_params,
            query_params=context.resolved_query_params,
            headers=context.resolved_headers,
            body=context.resolved_body,
            request_content_type = context.request_content_type,
            metadata={
                "role": context.role_context.get("role"),
                "intent": context.intent_metadata,
            },
        )

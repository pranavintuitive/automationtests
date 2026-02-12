# agent/resolution/context.py

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class StepResolutionContext:
    """
    Internal context passed through resolution pipeline.
    """

    endpoint: str
    http_method: str

    swagger_spec: Dict[str, Any]

    intent_metadata: Dict[str, Any]
    role_context: Dict[str, Any]

    execution_context: Dict[str, Any]

    deterministic_seed: Optional[int]

    # Populated during pipeline
    request_schema: Dict[str, Any] = field(default_factory=dict)
    required_fields: Dict[str, Any] = field(default_factory=dict)
    path_params_schema: Dict[str, Any] = field(default_factory=dict)
    query_params_schema: Dict[str, Any] = field(default_factory=dict)

    dependency_map: Dict[str, Any] = field(default_factory=dict)
    strategy_map: Dict[str, str] = field(default_factory=dict)

    resolved_body: Dict[str, Any] = field(default_factory=dict)
    resolved_headers: Dict[str, Any] = field(default_factory=dict)
    resolved_path_params: Dict[str, Any] = field(default_factory=dict)
    resolved_query_params: Dict[str, Any] = field(default_factory=dict)

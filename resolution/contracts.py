# agent/resolution/contracts.py

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TestStepResolutionRequest:
    """
    Input contract for Test Data Resolution Engine.
    """
    endpoint: str
    http_method: str
    swagger_spec: Dict[str, Any]

    intent_metadata: Dict[str, Any]
    role_context: Dict[str, Any]

    execution_context: Dict[str, Any] = field(default_factory=dict)
    deterministic_seed: Optional[int] = None
    request_content_type: Optional[str] = None

@dataclass
class ResolvedExecutionRequest:
    """
    Fully resolved request ready for execution.
    """
    url: str
    http_method: str
    path_params: Dict[str, Any] = field(default_factory=dict)
    query_params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, Any] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    request_content_type: Optional[str] = None

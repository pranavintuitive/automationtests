# agent/resolution/deterministic_binder.py

import random
from .context import StepResolutionContext


class DeterministicBinder:
    """
    Ensures deterministic behavior using provided seed.
    """

    def bind(self, context: StepResolutionContext) -> StepResolutionContext:
        if context.deterministic_seed is not None:
            random.seed(context.deterministic_seed)

        return context

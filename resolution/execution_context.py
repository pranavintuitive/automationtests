class ExecutionContext:
    """
    Stores dynamic resources captured during test execution.
    Used for lifecycle chaining.
    """

    def __init__(self):
        self.resources = {}

    def register(self, values: dict):
        if not values:
            return
        self.resources.update(values)

    def get(self, key: str):
        return self.resources.get(key)

    def has(self, key: str) -> bool:
        return key in self.resources

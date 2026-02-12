import json
from typing import List, Dict


class IntentModelBuilder:
    def __init__(self, behavior_report: List[Dict]):
        self.behavior_report = behavior_report
        self.intent_model = []

    # --------------------------------------------------
    # Public Build Method
    # --------------------------------------------------
    def build(self) -> List[Dict]:
        for ep in self.behavior_report:
            classified = self.classify_endpoint(ep)
            self.intent_model.append(classified)
        return self.intent_model

    # --------------------------------------------------
    # Classification Logic
    # --------------------------------------------------
    def classify_endpoint(self, ep: Dict) -> Dict:
        method = ep.get("method")
        path = ep.get("endpoint")

        classification = self.classify_by_method_and_path(method, path)
        risk = self.determine_risk(method, classification)
        test_types = self.determine_test_types(ep, classification)

        return {
            "endpoint": path,
            "method": method,
            "classification": classification,
            "risk_level": risk,
            "test_types": test_types,
            "roles": {
                "requires_auth": ep.get("auth", {}).get("requires_auth", False),
                "role_access": ep.get("auth", {}).get("role_access", {}),
            },
            "async": ep.get("async", False),
            "pagination": ep.get("pagination", False),
            "sorting": ep.get("sorting", False),
            "filtering": ep.get("filtering", False),
        }

    # --------------------------------------------------
    # Classification Heuristics
    # --------------------------------------------------
    def classify_by_method_and_path(self, method: str, path: str) -> str:
        method = method.upper()

        if method == "GET":
            if "search" in path or "filter" in path:
                return "search"
            return "read"

        if method == "POST":
            return "create"

        if method == "PUT" or method == "PATCH":
            return "update"

        if method == "DELETE":
            return "delete"

        return "other"

    # --------------------------------------------------
    # Risk Determination
    # --------------------------------------------------
    def determine_risk(self, method: str, classification: str) -> str:
        if method in ["DELETE"]:
            return "critical"

        if method in ["POST", "PUT", "PATCH"]:
            return "high"

        if classification == "search":
            return "medium"

        return "low"

    # --------------------------------------------------
    # Test Type Decision
    # --------------------------------------------------
    def determine_test_types(self, ep: Dict, classification: str) -> List[str]:
        test_types = ["contract"]

        if classification in ["create", "update", "delete"]:
            test_types.append("functional")

        if ep.get("roles", {}).get("requires_auth"):
            test_types.append("security")

        if ep.get("pagination"):
            test_types.append("pagination")

        if ep.get("sorting"):
            test_types.append("sorting")

        if ep.get("filtering"):
            test_types.append("filtering")

        return test_types

    # --------------------------------------------------
    # Safe Save (JSON-Safe)
    # --------------------------------------------------
    def save(self, file_path: str):
        safe_model = self.make_json_safe(self.intent_model)

        with open(file_path, "w") as f:
            json.dump(safe_model, f, indent=2)

        print("Intent model saved")

    # --------------------------------------------------
    # JSON Safety Converter
    # --------------------------------------------------
    def make_json_safe(self, obj):
        if isinstance(obj, dict):
            return {k: self.make_json_safe(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self.make_json_safe(v) for v in obj]

        # Convert any non-serializable object to string
        if not isinstance(obj, (str, int, float, bool, type(None))):
            return str(obj)

        return obj

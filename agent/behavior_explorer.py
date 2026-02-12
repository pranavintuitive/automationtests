import requests
from typing import Dict, List, Optional


class BehaviorExplorer:
    def __init__(
        self,
        base_url: str,
        endpoints: List[dict],
        role_headers: Optional[Dict[str, Dict]] = None,
        environment: str = "staging",
    ):
        self.base_url = base_url.rstrip("/")
        self.endpoints = endpoints
        self.role_headers = role_headers or {}
        self.environment = environment
        self.report = []

    # --------------------------------------------------
    # Entry Point
    # --------------------------------------------------
    def explore_all(self) -> List[dict]:
        for ep in self.endpoints:
            result = self.explore_endpoint(ep)
            if result:
                self.report.append(result)
        return self.report

    # --------------------------------------------------
    # Preferred Role Selection
    # --------------------------------------------------
    def get_preferred_role_headers(self) -> Dict:
        # Prefer admin if available
        if "admin" in self.role_headers:
            return self.role_headers["admin"]

        # Otherwise return first available role
        for headers in self.role_headers.values():
            return headers

        # No auth
        return {}

    # --------------------------------------------------
    # Endpoint Exploration
    # --------------------------------------------------
    def explore_endpoint(self, endpoint: dict) -> Optional[dict]:
        method = endpoint["method"].upper()
        path = endpoint["path"]
        full_url = f"{self.base_url}{path}"

        # Production safety guard
        if self.environment == "production" and method != "GET":
            return None

        behavior = {
            "endpoint": path,
            "method": method,
            "auth": self.detect_roles(method, full_url),
            "pagination": False,
            "sorting": False,
            "filtering": False,
            "async": False,
            "response_schema": None,
            "error_patterns": {},
        }

        headers = self.get_preferred_role_headers()
        response = self.safe_call(method, full_url, headers=headers)

        if not response:
            return behavior

        behavior["response_schema"] = self.capture_runtime_schema(response)
        behavior["pagination"] = self.detect_pagination(method, full_url)
        behavior["sorting"] = self.detect_sorting(method, full_url)
        behavior["filtering"] = self.detect_filtering(method, full_url)
        behavior["async"] = self.detect_async_behavior(response)
        behavior["error_patterns"] = self.detect_error_patterns(method, full_url)

        return behavior

    # --------------------------------------------------
    # Safe Call Wrapper
    # --------------------------------------------------
    def safe_call(self, method, url, **kwargs):
        try:
            return requests.request(method, url, timeout=10, **kwargs)
        except Exception:
            return None

    # --------------------------------------------------
    # Role Detection
    # --------------------------------------------------
    def detect_roles(self, method, url):
        role_access = {}

        # Check without authentication
        no_auth_response = self.safe_call(method, url)

        if no_auth_response is None:
            requires_auth = False
        else:
            requires_auth = no_auth_response.status_code in (401, 403)

        # Check each role
        for role_name, headers in self.role_headers.items():
            response = self.safe_call(method, url, headers=headers)

            if response is None:
                role_access[role_name] = False
                continue

            # Explicit authorization failure
            if response.status_code in (401, 403):
                role_access[role_name] = False
            else:
                role_access[role_name] = True

        return {
            "requires_auth": bool(requires_auth),
            "role_access": role_access,
        }


    # --------------------------------------------------
    # Pagination Detection
    # --------------------------------------------------
    def detect_pagination(self, method, url):
        headers = self.get_preferred_role_headers()

        r1 = self.safe_call(method, f"{url}?page=1&limit=5", headers=headers)
        r2 = self.safe_call(method, f"{url}?page=2&limit=5", headers=headers)

        if not r1 or not r2:
            return False

        return r1.status_code == 200 and r2.status_code == 200

    # --------------------------------------------------
    # Sorting Detection
    # --------------------------------------------------
    def detect_sorting(self, method, url):
        headers = self.get_preferred_role_headers()

        r = self.safe_call(method, f"{url}?sort=id&order=desc", headers=headers)
        return r and r.status_code == 200

    # --------------------------------------------------
    # Filtering Detection
    # --------------------------------------------------
    def detect_filtering(self, method, url):
        headers = self.get_preferred_role_headers()

        r = self.safe_call(method, f"{url}?filter=test", headers=headers)
        return r and r.status_code == 200

    # --------------------------------------------------
    # Async Detection
    # --------------------------------------------------
    def detect_async_behavior(self, response):
        return response.status_code == 202

    # --------------------------------------------------
    # Error Pattern Capture
    # --------------------------------------------------
    def detect_error_patterns(self, method, url):
        headers = self.get_preferred_role_headers()
        errors = {}

        r = self.safe_call(method, url + "/invalid", headers=headers)
        if r:
            errors[str(r.status_code)] = {
                "status_code": r.status_code,
                "body": r.text[:300],
            }

        return errors

    # --------------------------------------------------
    # Runtime Schema Capture
    # --------------------------------------------------
    def capture_runtime_schema(self, response):
        try:
            data = response.json()
            return self.build_schema_from_json(data)
        except Exception:
            return None

    def build_schema_from_json(self, data):
        if isinstance(data, dict):
            return {
                "type": "object",
                "properties": {
                    k: self.build_schema_from_json(v)
                    for k, v in data.items()
                },
            }

        elif isinstance(data, list):
            if data:
                return {
                    "type": "array",
                    "items": self.build_schema_from_json(data[0]),
                }
            return {"type": "array"}

        elif isinstance(data, str):
            return {"type": "string"}

        elif isinstance(data, int):
            return {"type": "integer"}

        elif isinstance(data, bool):
            return {"type": "boolean"}

        else:
            return {"type": "null"}

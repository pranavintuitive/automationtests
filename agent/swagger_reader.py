import requests


def read_swagger(swagger_url: str) -> dict:
    response = requests.get(swagger_url, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_endpoints(spec: dict):
    base_url = spec.get("servers", [{}])[0].get("url", "")
    paths = spec.get("paths", {})

    endpoints = []

    for path, methods in paths.items():
        for method, details in methods.items():
            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "parameters": details.get("parameters", []),
                    "requestBody": details.get("requestBody"),
                    "responses": details.get("responses", {}),
                }
            )

    return base_url, endpoints

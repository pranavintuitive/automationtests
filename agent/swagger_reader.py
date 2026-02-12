import requests


def read_swagger(swagger_url: str) -> dict:
    response = requests.get(swagger_url, timeout=10)
    response.raise_for_status()
    return response.json()


def _extract_parameters(path_level_params, operation_level_params):
    """
    Merge path-level and operation-level parameters.
    Normalize schema structure to always include:
    name, in, required, type, format
    """
    merged = []

    all_params = (path_level_params or []) + (operation_level_params or [])

    for param in all_params:
        schema = param.get("schema", {})

        merged.append(
            {
                "name": param.get("name"),
                "in": param.get("in"),  # path | query | header | cookie
                "required": param.get("required", False),
                "type": schema.get("type"),
                "format": schema.get("format"),  # <---- critical for uuid
            }
        )

    return merged


def extract_endpoints(spec: dict):
    base_url = ""
    if spec.get("servers"):
        base_url = spec["servers"][0].get("url", "")

    paths = spec.get("paths", {})
    endpoints = []

    for path, path_item in paths.items():

        path_level_params = path_item.get("parameters", [])

        for method, details in path_item.items():

            if method.upper() not in {
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "OPTIONS",
                "HEAD",
            }:
                continue

            operation_level_params = details.get("parameters", [])

            normalized_params = _extract_parameters(
                path_level_params,
                operation_level_params,
            )

            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "parameters": normalized_params,
                    "requestBody": details.get("requestBody"),
                    "responses": details.get("responses", {}),
                }
            )

    return base_url, endpoints

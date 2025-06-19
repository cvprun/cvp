# -*- coding: utf-8 -*-

from typing import Any, Dict


def get_openapi_version(spec: Dict[str, Any]) -> str:
    if swagger := spec.get("swagger", None):
        return str(swagger)
    if openapi := spec.get("openapi", None):
        return str(openapi)
    else:
        raise ValueError("Invalid OpenAPI specification: version not found")


def is_openapi_3x(version_text: str) -> bool:
    return version_text.startswith("3.")

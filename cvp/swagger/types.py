# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional


def openapi_type_to_python_annotation(
    openapi_type: str,
    openapi_format: Optional[str] = None,
    openapi_items: Optional[Dict[str, Any]] = None,
) -> str:
    match openapi_type:
        case "integer":
            if openapi_format == "int64":
                return "int"
            else:
                return "int"

        case "number":
            if openapi_format == "float":
                return "float"
            elif openapi_format == "double":
                return "float"
            else:
                return "float"

        case "string":
            if openapi_format == "date":
                return "datetime.date"
            elif openapi_format == "date-time":
                return "datetime.datetime"
            elif openapi_format == "binary":
                return "bytes"
            else:
                return "str"

        case "boolean":
            return "bool"

        case "array":
            if openapi_items and "type" in openapi_items:
                item_annotation = openapi_type_to_python_annotation(
                    openapi_items["type"],
                    openapi_items.get("format"),
                    openapi_items.get("items"),
                )
                return f"typing.List[{item_annotation}]"
            else:
                return "typing.List[typing.Any]"

        case "object":
            return "typing.Dict[str, typing.Any]"

        case "null":
            return "None"

        case _:
            return "typing.Any"

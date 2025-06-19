# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional


def map_openapi_type_to_python(
    openapi_type: str,
    fmt: Optional[str] = None,
    items: Optional[Dict[str, Any]] = None,
) -> str:
    match openapi_type:
        case "integer":
            if fmt == "int64":
                return "int"
            else:
                return "int"

        case "number":
            if fmt == "float":
                return "float"
            elif fmt == "double":
                return "float"
            else:
                return "float"

        case "string":
            if fmt == "date":
                return "datetime.date"
            elif fmt == "date-time":
                return "datetime.datetime"
            elif fmt == "binary":
                return "bytes"
            else:
                return "str"

        case "boolean":
            return "bool"

        case "array":
            if items and "type" in items:
                item_type = map_openapi_type_to_python(
                    items["type"],
                    items.get("format"),
                    items.get("items"),
                )
                return f"List[{item_type}]"
            else:
                return "List[Any]"

        case "object":
            return "Dict[str, Any]"

        case "null":
            return "None"

        case _:
            return "Any"

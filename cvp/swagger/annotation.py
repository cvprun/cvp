# -*- coding: utf-8 -*-

from functools import reduce
from typing import Any, Iterable, List, Optional, Union

from cvp.swagger.schemas.v3 import ReferenceObject, SchemaObject


def openapi_enum_to_python_literal(openapi_enum: Iterable[Any]) -> str:
    quoted = [f'"{e}"' for e in openapi_enum]
    merged = reduce(lambda x, y: f"{x}, {y}", quoted[1:], quoted[0])
    return f"typing.Literal[{merged}]"


def openapi_type_to_python_annotation(
    openapi_type: Optional[str] = None,
    openapi_format: Optional[str] = None,
    openapi_enum: Optional[List[Any]] = None,
    openapi_items: Optional[Union[SchemaObject, ReferenceObject]] = None,
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
                if openapi_enum:
                    return openapi_enum_to_python_literal(openapi_enum)
                else:
                    return "str"

        case "boolean":
            return "bool"

        case "array":
            if isinstance(openapi_items, SchemaObject):
                item_annotation = openapi_type_to_python_annotation(
                    openapi_type=openapi_items.type,
                    openapi_format=openapi_items.format,
                    openapi_enum=openapi_items.enum,
                    openapi_items=openapi_items.items,
                )
                if openapi_items.nullable:
                    return f"typing.List[typing.Optional[{item_annotation}]]"
                else:
                    return f"typing.List[{item_annotation}]"
            elif isinstance(openapi_items, ReferenceObject):
                if openapi_items.ref.startswith("#/components/schemas/"):
                    ref = openapi_items.ref.removeprefix("#/components/schemas/")
                    return f'typing.List["{ref}"]'
                else:
                    return "typing.List[typing.Any]"
            else:
                return "typing.List[typing.Any]"

        case "object":
            return "typing.Dict[str, typing.Any]"

        case "null":
            return "None"

        case _:
            return "typing.Any"


def openapi_schema_to_python_annotation(schema: SchemaObject) -> str:
    return openapi_type_to_python_annotation(
        openapi_type=schema.type,
        openapi_format=schema.format,
        openapi_enum=schema.enum,
        openapi_items=schema.items,
    )

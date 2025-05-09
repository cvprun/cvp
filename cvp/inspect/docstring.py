# -*- coding: utf-8 -*-

from ast import AnnAssign, Expr, parse
from dataclasses import fields, is_dataclass
from inspect import cleandoc, getsource
from typing import Any, Dict, Optional


def get_attribute_docstring(cls: type, key: str) -> Optional[str]:
    src = getsource(cls)
    module = parse(src)
    module_body = module.body

    assert len(module_body) == 1
    module_body0 = module_body[0]

    assert module_body0.name == cls.__name__  # type: ignore[attr-defined]
    stmts = module_body0.body  # type: ignore[attr-defined]
    assert isinstance(stmts, list)

    for i, stmt in enumerate(stmts):
        if not isinstance(stmt, AnnAssign):
            continue
        if stmt.target.id != key:  # type: ignore[union-attr]
            continue

        try:
            expr = stmts[i + 1]
        except IndexError:
            return None

        if not isinstance(expr, Expr):
            return None

        doc_value = expr.value.value  # type: ignore[attr-defined]
        if not isinstance(doc_value, str):
            return None

        return cleandoc(doc_value)

    return None


def generate_dataclass_fields_docs(props: Any) -> Dict[str, Optional[str]]:
    assert is_dataclass(props)
    cls = type(props)
    result = dict()
    for field in fields(cls):  # type: ignore[arg-type]
        result[field.name] = get_attribute_docstring(cls, field.name)
    return result

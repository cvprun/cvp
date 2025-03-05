# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/functions.html

from functools import lru_cache
from typing import Callable, Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_builtin_functions() -> Sequence[Callable]:
    return (
        abs,
        all,
        any,
        ascii,
        bin,
        chr,
        complex,
        divmod,
        enumerate,
        format,
        hash,
        hex,
        id,
        isinstance,
        issubclass,
        len,
        oct,
        open,
        ord,
        pow,
        print,
        property,
        repr,
        reversed,
        round,
        sorted,
        sum,
    )


def get_builtin_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    result = list()
    for func in get_builtin_functions():
        node = NodeTemplate.auto_parse(func, dtype_registry=dtype_registry)
        result.append(node)
    return tuple(result)

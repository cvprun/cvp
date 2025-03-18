# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/functions.html

from functools import lru_cache
from typing import Callable, Sequence

from cvp.nodes.callable import CallableNode


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


def get_builtin_nodes() -> Sequence[CallableNode]:
    return tuple(CallableNode(func) for func in get_builtin_functions())

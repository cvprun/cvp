# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/functions.html

from typing import Callable, Sequence


def get_builtin_functions() -> Sequence[Callable]:
    return [
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
    ]

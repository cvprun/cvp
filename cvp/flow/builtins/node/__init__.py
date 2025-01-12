# -*- coding: utf-8 -*-

from typing import Callable, List


def get_builtin_functions() -> List[Callable]:
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

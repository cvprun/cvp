# -*- coding: utf-8 -*-

from functools import reduce
from typing import Any, Iterable


def join_iterable(iterable: Iterable[Any], delimiter: str) -> str:
    if iterable:
        strings = map(lambda x: str(x), iterable)
        return reduce(lambda x, y: f"{x}{delimiter}{y}", strings)
    else:
        return str()

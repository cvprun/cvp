# -*- coding: utf-8 -*-

from inspect import isfunction
from types import LambdaType


def islambda(o) -> bool:
    return isfunction(o) and isinstance(o, LambdaType) and o.__name__ == "<lambda>"

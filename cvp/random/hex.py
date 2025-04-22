# -*- coding: utf-8 -*-

from functools import reduce
from random import choices
from string import hexdigits


def generate_hexdigits(k: int) -> str:
    return reduce(lambda x, y: x + y, choices(hexdigits, k=k))

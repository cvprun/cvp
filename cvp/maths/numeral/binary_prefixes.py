# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Binary_prefix

from functools import lru_cache
from math import floor, log
from types import MappingProxyType
from typing import Final, Tuple

from cvp.maths.numeral.metric_prefix import MetricPrefix


def _create_binary_prefixes():
    return (
        MetricPrefix(base=2, exponent=100, name="quetta", symbol="Q"),
        MetricPrefix(base=2, exponent=90, name="ronna", symbol="R"),
        MetricPrefix(base=2, exponent=80, name="yotta", symbol="Y"),
        MetricPrefix(base=2, exponent=70, name="zetta", symbol="Z"),
        MetricPrefix(base=2, exponent=60, name="exa", symbol="E"),
        MetricPrefix(base=2, exponent=50, name="peta", symbol="P"),
        MetricPrefix(base=2, exponent=40, name="tera", symbol="T"),
        MetricPrefix(base=2, exponent=30, name="giga", symbol="G"),
        MetricPrefix(base=2, exponent=20, name="mega", symbol="M"),
        MetricPrefix(base=2, exponent=10, name="kilo", symbol="K"),
        MetricPrefix(base=2, exponent=0, name="", symbol=""),
    )


@lru_cache
def _binary_prefixes() -> MappingProxyType[int, MetricPrefix]:
    return MappingProxyType({si.exponent: si for si in _create_binary_prefixes()})


BINARY_PREFIXES: Final[MappingProxyType[int, MetricPrefix]] = _binary_prefixes()

MAX_BINARY_PREFIX_EXPONENT: Final[int] = max(BINARY_PREFIXES.keys())
MIN_BINARY_PREFIX_EXPONENT: Final[int] = min(BINARY_PREFIXES.keys())


def binary_prefix_with_integer(value: int) -> Tuple[int, MetricPrefix]:
    if value == 0:
        return 0, BINARY_PREFIXES[0]

    # log2(value) / log2(1024) = log1024(value) = log(value, 1024)
    exponent_power = int(floor(log(abs(value), 1024)))
    binary_exponent = exponent_power * 10

    binary_exponent = min(binary_exponent, MAX_BINARY_PREFIX_EXPONENT)
    binary_exponent = max(binary_exponent, MIN_BINARY_PREFIX_EXPONENT)

    scaled = int(floor(value / (1024 ** (binary_exponent // 10))))
    prefix = BINARY_PREFIXES[binary_exponent]
    return scaled, prefix

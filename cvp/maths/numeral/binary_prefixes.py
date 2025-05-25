# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Binary_prefix

from functools import lru_cache
from types import MappingProxyType
from typing import Final

from cvp.maths.numeral.metric_prefix import MetricPrefix, calc_exponent_index


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
BINARY_PREFIXES_BASE: Final[int] = 2
BINARY_PREFIXES_EXPONENT_STEP: Final[int] = 10
BINARY_PREFIXES_FORMAT_PRECISION: Final[int] = 2
BINARY_PREFIXES_FORMAT_SUFFIX: Final[str] = "B"
MAX_BINARY_PREFIX_EXPONENT: Final[int] = max(BINARY_PREFIXES.keys())
MIN_BINARY_PREFIX_EXPONENT: Final[int] = min(BINARY_PREFIXES.keys())

BYTES_IN_KB: Final[int] = BINARY_PREFIXES[10].factor
BYTES_IN_MB: Final[int] = BINARY_PREFIXES[20].factor
BYTES_IN_GB: Final[int] = BINARY_PREFIXES[30].factor
BYTES_IN_TB: Final[int] = BINARY_PREFIXES[40].factor
BYTES_IN_PB: Final[int] = BINARY_PREFIXES[50].factor
BYTES_IN_EB: Final[int] = BINARY_PREFIXES[60].factor
BYTES_IN_ZB: Final[int] = BINARY_PREFIXES[70].factor
BYTES_IN_YB: Final[int] = BINARY_PREFIXES[80].factor
BYTES_IN_RB: Final[int] = BINARY_PREFIXES[90].factor
BYTES_IN_QB: Final[int] = BINARY_PREFIXES[100].factor


def parse_binary_prefix(value: int) -> MetricPrefix:
    index = calc_exponent_index(
        value=value,
        base=BINARY_PREFIXES_BASE,
        step_exponent=BINARY_PREFIXES_EXPONENT_STEP,
        min_exponent=MIN_BINARY_PREFIX_EXPONENT,
        max_exponent=MAX_BINARY_PREFIX_EXPONENT,
    )
    return BINARY_PREFIXES[index]


def format_binary_prefix(
    value: int,
    *,
    precision=BINARY_PREFIXES_FORMAT_PRECISION,
    suffix=BINARY_PREFIXES_FORMAT_SUFFIX,
) -> str:
    prefix = parse_binary_prefix(value)
    return prefix.format_scale(value, precision=precision, suffix=suffix)

# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/International_System_of_Units#Prefixes

from functools import lru_cache
from math import floor, log10
from types import MappingProxyType
from typing import Final, Tuple

from cvp.maths.numeral.metric_prefix import MetricPrefix


def _create_si_prefixes():
    return (
        MetricPrefix(base=10, exponent=30, name="quetta", symbol="Q"),
        MetricPrefix(base=10, exponent=27, name="ronna", symbol="R"),
        MetricPrefix(base=10, exponent=24, name="yotta", symbol="Y"),
        MetricPrefix(base=10, exponent=21, name="zetta", symbol="Z"),
        MetricPrefix(base=10, exponent=18, name="exa", symbol="E"),
        MetricPrefix(base=10, exponent=15, name="peta", symbol="P"),
        MetricPrefix(base=10, exponent=12, name="tera", symbol="T"),
        MetricPrefix(base=10, exponent=9, name="giga", symbol="G"),
        MetricPrefix(base=10, exponent=6, name="mega", symbol="M"),
        MetricPrefix(base=10, exponent=3, name="kilo", symbol="k"),
        MetricPrefix(base=10, exponent=2, name="hecto", symbol="h"),
        MetricPrefix(base=10, exponent=1, name="deca", symbol="da"),
        MetricPrefix(base=10, exponent=0, name="", symbol=""),
        MetricPrefix(base=10, exponent=-1, name="deci", symbol="d"),
        MetricPrefix(base=10, exponent=-2, name="centi", symbol="c"),
        MetricPrefix(base=10, exponent=-3, name="milli", symbol="m"),
        MetricPrefix(base=10, exponent=-6, name="micro", symbol="μ"),
        MetricPrefix(base=10, exponent=-9, name="nano", symbol="n"),
        MetricPrefix(base=10, exponent=-12, name="pico", symbol="p"),
        MetricPrefix(base=10, exponent=-15, name="femto", symbol="f"),
        MetricPrefix(base=10, exponent=-18, name="atto", symbol="a"),
        MetricPrefix(base=10, exponent=-21, name="zepto", symbol="z"),
        MetricPrefix(base=10, exponent=-24, name="yocto", symbol="y"),
        MetricPrefix(base=10, exponent=-27, name="ronto", symbol="r"),
        MetricPrefix(base=10, exponent=-30, name="quecto", symbol="q"),
    )


@lru_cache
def _si_prefixes() -> MappingProxyType[int, MetricPrefix]:
    return MappingProxyType({si.exponent: si for si in _create_si_prefixes()})


SI_PREFIXES: Final[MappingProxyType[int, MetricPrefix]] = _si_prefixes()

MAX_SI_PREFIX_EXPONENT: Final[int] = max(SI_PREFIXES.keys())
MIN_SI_PREFIX_EXPONENT: Final[int] = min(SI_PREFIXES.keys())


def si_prefix_with_integer(value: int) -> Tuple[int, MetricPrefix]:
    if value == 0:
        return 0, SI_PREFIXES[0]

    exponent = int(floor(log10(abs(value)) // 3 * 3))
    exponent = max(min(exponent, MAX_SI_PREFIX_EXPONENT), 0)

    scaled = int(floor(value / (10**exponent)))
    prefix = SI_PREFIXES[exponent]
    return scaled, prefix

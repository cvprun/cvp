# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/International_System_of_Units#Prefixes

from functools import lru_cache
from types import MappingProxyType
from typing import Final

from cvp.maths.numeral.metric_prefix import MetricPrefix, calc_exponent_index


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
SI_PREFIXES_BASE: Final[int] = 10
SI_PREFIXES_EXPONENT_STEP: Final[int] = 3
SI_PREFIXES_FORMAT_PRECISION: Final[int] = 3
SI_PREFIXES_FORMAT_SUFFIX: Final[str] = ""
MAX_SI_PREFIX_EXPONENT: Final[int] = max(SI_PREFIXES.keys())
MIN_SI_PREFIX_EXPONENT: Final[int] = min(SI_PREFIXES.keys())

QUETTA: Final[int] = SI_PREFIXES[30].factor
RONNA: Final[int] = SI_PREFIXES[27].factor
YOTTA: Final[int] = SI_PREFIXES[24].factor
ZETTA: Final[int] = SI_PREFIXES[21].factor
EXA: Final[int] = SI_PREFIXES[18].factor
PETA: Final[int] = SI_PREFIXES[15].factor
TERA: Final[int] = SI_PREFIXES[12].factor
GIGA: Final[int] = SI_PREFIXES[9].factor
MEGA: Final[int] = SI_PREFIXES[6].factor
KILO: Final[int] = SI_PREFIXES[3].factor
HECTO: Final[int] = SI_PREFIXES[2].factor
DECA: Final[int] = SI_PREFIXES[1].factor

DECI: Final[int] = SI_PREFIXES[-1].factor
CENTI: Final[int] = SI_PREFIXES[-2].factor
MILLI: Final[int] = SI_PREFIXES[-3].factor
MICRO: Final[int] = SI_PREFIXES[-6].factor
NANO: Final[int] = SI_PREFIXES[-9].factor
PICO: Final[int] = SI_PREFIXES[-12].factor
FEMTO: Final[int] = SI_PREFIXES[-15].factor
ATTO: Final[int] = SI_PREFIXES[-18].factor
ZEPTO: Final[int] = SI_PREFIXES[-21].factor
YOCTO: Final[int] = SI_PREFIXES[-24].factor
RONTO: Final[int] = SI_PREFIXES[-27].factor
QUECTO: Final[int] = SI_PREFIXES[-30].factor


def parse_si_prefix(value: int) -> MetricPrefix:
    index = calc_exponent_index(
        value=value,
        base=SI_PREFIXES_BASE,
        step_exponent=SI_PREFIXES_EXPONENT_STEP,
        min_exponent=MIN_SI_PREFIX_EXPONENT,
        max_exponent=MAX_SI_PREFIX_EXPONENT,
    )
    return SI_PREFIXES[index]


def format_si_prefix(
    value: int,
    *,
    precision=SI_PREFIXES_FORMAT_PRECISION,
    suffix=SI_PREFIXES_FORMAT_SUFFIX,
) -> str:
    prefix = parse_si_prefix(value)
    return prefix.format_scale(value, precision=precision, suffix=suffix)

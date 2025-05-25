# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Metric_prefix

from decimal import Decimal, getcontext
from math import floor, log, log2, log10
from sys import float_info
from typing import Final, NamedTuple, Optional

from cvp.maths.decimals.trunc import floating_round_down

_HIGH_PRECISION_PRECISION: Final[int] = 32


class MetricPrefix(NamedTuple):
    base: int
    exponent: int
    name: str
    symbol: str

    @property
    def factor(self) -> int:
        return pow(self.base, self.exponent)

    @property
    def sym0(self) -> str:
        return self.symbol[0] if self.symbol else str()

    def scale(self, value: int) -> float:
        return value / self.factor

    def scale_text(self, value: int, precision: Optional[int] = None) -> str:
        if precision is not None:
            if precision == 0:
                return str(floor(self.scale(value)))
            else:
                return str(floating_round_down(self.scale(value), precision))
        else:
            return str(self.scale(value))

    def format_scale(self, value: int, *, precision=0, suffix="") -> str:
        if precision < 0:
            raise ValueError("Precision must be a positive integer")

        scaled_text = self.scale_text(value, precision)
        return f"{scaled_text}{self.symbol}{suffix}"


def calc_exponent_with_decimal(
    value: int,
    base: int,
    min_precision: Optional[int] = _HIGH_PRECISION_PRECISION,
):
    """
    Calculates the exponent of a number with high precision.
    """

    if min_precision is not None:
        decimal_context = getcontext()

        if decimal_context.prec < min_precision:
            # noinspection SpellCheckingInspection
            decimal_context.prec = min_precision

    # Calculates using the logarithm base change formula with `Decimal`.
    # log_b(a) = log_x(a) / log_x(b) = ln(a) / ln(b)
    return floor(Decimal(value).ln() / Decimal(base).ln())


def calc_exponent(value: int, base: int, epsilon=float_info.epsilon) -> int:
    if value % base != 0:
        return calc_exponent_with_decimal(value, base)

    match base:
        case 2:
            return floor(log2(abs(value)))
        case 10:
            # log10(x) is more accurate than log(x, 10). As an example, log10(1000)
            # returns 3.0, whereas log(1000, 10) returns 2.9999999999999996.
            return floor(log10(abs(value)))
        case _:
            return floor(log(abs(value), base) + epsilon)


def calc_exponent_index(
    value: int,
    base: int,
    step_exponent: int,
    min_exponent: int,
    max_exponent: int,
) -> int:
    if value == 0:
        return 0
    exponent = calc_exponent(value, base) // step_exponent * step_exponent
    assert isinstance(exponent, int)
    exponent = min(exponent, max_exponent)
    exponent = max(exponent, min_exponent)
    return exponent

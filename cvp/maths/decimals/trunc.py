# -*- coding: utf-8 -*-

from decimal import ROUND_DOWN, ROUND_UP, Decimal
from typing import Optional


def quantize_exponent(precision: int) -> Decimal:
    return Decimal(str(1 / (10**precision)))


def floating_round(
    value: float,
    precision: int,
    rounding: Optional[str] = None,
) -> Decimal:
    decimal = Decimal(str(value))
    exp = quantize_exponent(precision)
    return decimal.quantize(exp, rounding=rounding)


def floating_round_down(value: float, precision: int) -> Decimal:
    return floating_round(value, precision, ROUND_DOWN)


def floating_round_up(value: float, precision: int) -> Decimal:
    return floating_round(value, precision, ROUND_UP)

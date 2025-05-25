# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Metric_prefix

from typing import NamedTuple


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

# -*- coding: utf-8 -*-

from math import sqrt


def l1_norm(x1: float, y1: float, x2: float, y2: float) -> float:
    return abs(x2 - x1) + abs(y2 - y1)


def l2_norm(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def max_norm(x1: float, y1: float, x2: float, y2: float) -> float:
    return max(abs(x2 - x1), abs(y2 - y1))

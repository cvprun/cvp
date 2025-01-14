# -*- coding: utf-8 -*-

from enum import StrEnum, unique


@unique
class Prefix(StrEnum):
    none = ""
    dtype = "&"
    graph = "#"
    node = "@"
    pin = "."
    arc = "-"

# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class ParamKind(StrEnum):
    positional_only = auto()
    positional_or_keyword = auto()
    var_positional = auto()
    keyword_only = auto()
    var_keyword = auto()

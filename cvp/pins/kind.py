# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique
from inspect import Parameter


@unique
class PinKind(IntEnum):
    positional_only = Parameter.POSITIONAL_ONLY.value  # 0
    positional_or_keyword = Parameter.POSITIONAL_OR_KEYWORD.value  # 1
    var_positional = Parameter.VAR_POSITIONAL.value  # 2
    keyword_only = Parameter.KEYWORD_ONLY.value  # 3
    var_keyword = Parameter.VAR_KEYWORD.value  # 4
    return_only = auto()  # 5
    exec_only = auto()  # 6
    unknown = auto()


def parameter_to_kind(parameter: Parameter) -> PinKind:
    match parameter.kind:
        case Parameter.POSITIONAL_ONLY:
            return PinKind.positional_only
        case Parameter.POSITIONAL_OR_KEYWORD:
            return PinKind.positional_or_keyword
        case Parameter.VAR_POSITIONAL:
            return PinKind.var_positional
        case Parameter.KEYWORD_ONLY:
            return PinKind.keyword_only
        case Parameter.VAR_KEYWORD:
            return PinKind.var_keyword
        case _:
            assert False, "Inaccessible section"


def kind_to_parameter(kind: PinKind):
    match kind:
        case PinKind.positional_only:
            return Parameter.POSITIONAL_ONLY
        case PinKind.positional_or_keyword:
            return Parameter.POSITIONAL_OR_KEYWORD
        case PinKind.var_positional:
            return Parameter.VAR_POSITIONAL
        case PinKind.keyword_only:
            return Parameter.KEYWORD_ONLY
        case PinKind.var_keyword:
            return Parameter.VAR_KEYWORD
        case _:
            raise ValueError(f"Unexpected pin-kind: '{kind.name}'")

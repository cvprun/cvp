# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique
from inspect import Parameter


@unique
class PinKind(IntEnum):
    positional_only = Parameter.POSITIONAL_ONLY.value
    positional_or_keyword = Parameter.POSITIONAL_OR_KEYWORD.value
    var_positional = Parameter.VAR_POSITIONAL.value
    keyword_only = Parameter.KEYWORD_ONLY.value
    var_keyword = Parameter.VAR_KEYWORD.value
    return_only = auto()
    flow_only = auto()
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
            raise ValueError(f"Unexpected parameter kind: {parameter.kind}")


def kind_to_parameter(kind: PinKind):
    match kind:
        case PinKind.unknown:
            raise ValueError(f"Unsupported '{PinKind.unknown.name}' pin")
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
        case PinKind.return_only:
            raise ValueError(f"Unsupported '{PinKind.return_only.name}' pin")
        case PinKind.flow_only:
            raise ValueError(f"Unsupported '{PinKind.flow_only.name}' pin")
        case _:
            raise ValueError(f"Unexpected pin kind: '{kind.name}'")

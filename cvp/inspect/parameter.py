# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, Final

NoDefault: Final[Any] = Parameter.empty


def inspect_parameter_required(parameter: Parameter) -> bool:
    match parameter.kind:
        case Parameter.POSITIONAL_ONLY:
            return parameter.default == Parameter.empty
        case Parameter.POSITIONAL_OR_KEYWORD:
            return parameter.default == Parameter.empty
        case Parameter.VAR_POSITIONAL:
            return False
        case Parameter.KEYWORD_ONLY:
            return parameter.default == Parameter.empty
        case Parameter.VAR_KEYWORD:
            return False
        case _:
            raise ValueError(f"Unexpected parameter kind: {parameter.kind}")

# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Literal, Union


@unique
class Action(StrEnum):
    exec = auto()
    """
    Execution pins are used to connect nodes together to create a flow of execution.
    """

    data = auto()
    """
    Data pins are used for taking data into a node or outputting data from a node.
    """


ActionLiteral = Literal["exec", "data", 0, 1]
AnyAction = Union[Action, ActionLiteral]


def create_action(value: AnyAction) -> Action:
    if isinstance(value, Action):
        return value
    elif isinstance(value, str):
        match value.lower():
            case "exec":
                return Action.exec
            case "data":
                return Action.data
            case _:
                raise ValueError(f"Unsupported action value: {value}")
    elif isinstance(value, int):
        match value:
            case 0:
                return Action.exec
            case 1:
                return Action.data
            case _:
                raise ValueError(f"Unsupported action value: {value}")
    else:
        raise TypeError(f"Unsupported action type: {type(value).__name__}")

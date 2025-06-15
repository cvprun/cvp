# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique
from typing import Final, Union

from cvp.debugging.markers import __MSG_ADD_A_NEW_TODO__
from cvp.types.enum.normalize.number import (
    FrozenNameToNumber,
    FrozenNumberToName,
    name2number,
    normalize_name2number,
    normalize_number2name,
    number2name,
)


@unique
class MsgType(IntEnum):
    none = 0

    # Toast message events
    toast = auto()

    # Watchdog's filesystem events
    file_moved = auto()
    file_created = auto()
    file_deleted = auto()
    file_modified = auto()
    file_closed = auto()
    file_closed_no_write = auto()
    file_opened = auto()

    # Process events
    process_exited = auto()

    # Scheduler events
    job_scheduled = auto()
    job_completed = auto()

    assert __MSG_ADD_A_NEW_TODO__, "Insert the 'msg' name here"


MSG_TYPE_NAME_TO_NUMBER: Final[FrozenNameToNumber] = name2number(MsgType)
MSG_TYPE_NUMBER_TO_NAME: Final[FrozenNumberToName] = number2name(MsgType)

MsgTypeLike = Union[MsgType, IntEnum, str, int]


def get_msg_type_number(value: MsgTypeLike) -> int:
    return normalize_name2number(MSG_TYPE_NAME_TO_NUMBER, value)


def get_msg_type_name(value: MsgTypeLike) -> str:
    return normalize_number2name(MSG_TYPE_NUMBER_TO_NAME, value)


def normalize_msg_type(value: MsgTypeLike) -> MsgType:
    if isinstance(value, MsgType):
        return value
    elif isinstance(value, (IntEnum, int)):
        return MsgType(int(value))
    elif isinstance(value, str):
        return MsgType(MSG_TYPE_NAME_TO_NUMBER[value])
    else:
        raise TypeError(f"Unsupported value type: {type(value).__name__}")

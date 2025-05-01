# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Any, Dict, Final, NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.cond import Cond
from cvp.imgui.flags.drag_drop import DragDropFlags
from cvp.patterns.singleton import singleton

UNDEFINED_PAYLOAD_ID: Final[int] = 0


@singleton
class GlobalDragDropPayloadMapper(Dict[str, Any]):
    pass


@lru_cache
def global_drag_drop_payload_mapper():
    return GlobalDragDropPayloadMapper()


class DragDropPayload(NamedTuple):
    accepted: bool
    type: str
    data_id: int
    value: Any

    @classmethod
    def from_none(cls):
        return cls(False, str(), UNDEFINED_PAYLOAD_ID, None)

    @classmethod
    def from_raw(cls, result: Optional[imgui.Payload_PyId] = None, value=None):
        if result is not None:
            return cls(True, result.type, result.data_id, value)
        else:
            return cls.from_none()

    def __bool__(self):
        return self.accepted


def accept_payload_id(type_: str, flags: Union[DragDropFlags, int] = 0):
    if isinstance(flags, DragDropFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.accept_drag_drop_payload_py_id(type_, flags)
    return DragDropPayload.from_raw(result)


def accept_payload(type_: str, flags: Union[DragDropFlags, int] = 0):
    result = accept_payload_id(type_, flags)
    assert result.data_id == UNDEFINED_PAYLOAD_ID
    return DragDropPayload(
        result.accepted,
        result.type,
        result.data_id,
        global_drag_drop_payload_mapper().get(type_),
    )


def begin_target() -> bool:
    return imgui.begin_drag_drop_target()


def end_target() -> None:
    return imgui.end_drag_drop_target()


def set_payload_id(type_: str, data_id: int, cond: Union[Cond, int] = 0) -> bool:
    if isinstance(cond, Cond):
        cond = int(cond)
    assert isinstance(cond, int)
    return imgui.set_drag_drop_payload_py_id(type_, data_id, cond)


def set_payload(type_: str, data: Any, cond: Union[Cond, int] = 0) -> bool:
    global_drag_drop_payload_mapper()[type_] = data
    return set_payload_id(type_, UNDEFINED_PAYLOAD_ID, cond)


def begin_source(flags: Union[DragDropFlags, int] = 0) -> bool:
    if isinstance(flags, DragDropFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    return imgui.begin_drag_drop_source(flags)


def end_source() -> None:
    return imgui.end_drag_drop_source()

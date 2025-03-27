# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.window import WindowFlags


class BeginResult(NamedTuple):
    opened: bool
    value: Optional[bool]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, (type(None), bool))
        return cls(changed, value)

    def __bool__(self):
        return self.opened


def begin(
    label: str,
    closable: Optional[bool] = None,
    flags: Union[WindowFlags, int] = 0,
):
    result = imgui.begin(label, closable, flags)
    return BeginResult.from_raw(result)


def end() -> None:
    imgui.end()


@contextmanager
def begin_context(
    label: str,
    closable: Optional[bool] = None,
    flags: Union[WindowFlags, int] = 0,
):
    result = begin(label, closable, flags)
    try:
        yield result
    finally:
        end()

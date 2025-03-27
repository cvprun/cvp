# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.child import ChildFlags
from cvp.imgui.flags.window import WindowFlags


def begin_child(
    label: Union[str, int],
    width=0.0,
    height=0.0,
    child_flags: Union[ChildFlags, int] = 0,
    window_flags: Union[WindowFlags, int] = 0,
) -> bool:
    return imgui.begin_child(label, (width, height), child_flags, window_flags)


def end_child() -> None:
    imgui.end_child()


@contextmanager
def begin_child_context(
    label: Union[str, int],
    width=0.0,
    height=0.0,
    child_flags: Union[ChildFlags, int] = 0,
    window_flags: Union[WindowFlags, int] = 0,
):
    result = begin_child(label, width, height, child_flags, window_flags)
    try:
        yield result
    finally:
        end_child()

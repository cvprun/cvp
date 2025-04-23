# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.child import ChildFlags
from cvp.imgui.flags.window import WindowFlags


def begin_child(
    label: Union[str, int],
    size: Optional[imgui.ImVec2Like] = None,
    child_flags: Union[ChildFlags, int] = 0,
    window_flags: Union[WindowFlags, int] = 0,
) -> bool:
    if isinstance(child_flags, ChildFlags):
        child_flags = int(child_flags)
    if isinstance(window_flags, WindowFlags):
        window_flags = int(window_flags)

    assert isinstance(child_flags, int)
    assert isinstance(window_flags, int)

    return imgui.begin_child(label, size, child_flags, window_flags)


def end_child() -> None:
    imgui.end_child()


@contextmanager
def begin_child_context(
    label: Union[str, int],
    size: Optional[imgui.ImVec2Like] = None,
    child_flags: Union[ChildFlags, int] = 0,
    window_flags: Union[WindowFlags, int] = 0,
):
    result = begin_child(label, size, child_flags, window_flags)
    try:
        yield result
    finally:
        end_child()

# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.dock_node import PASSTHRU_CENTRAL_NODE, DockNodeFlags
from cvp.imgui.get_id import get_id


@contextmanager
def dockspace_over_viewport_context(
    dock_space_id: Optional[Union[str, int]] = None,
    viewport: Optional[imgui.Viewport] = None,
    flags: Union[DockNodeFlags, int] = PASSTHRU_CENTRAL_NODE,
    window_class: Optional[imgui.WindowClass] = None,
):
    if isinstance(flags, DockNodeFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    id_ = imgui.dock_space_over_viewport(
        get_id(dock_space_id),
        viewport if viewport is not None else imgui.get_main_viewport(),
        flags,
        window_class,
    )

    imgui.push_id(id_)
    try:
        yield id_
    finally:
        imgui.pop_id()

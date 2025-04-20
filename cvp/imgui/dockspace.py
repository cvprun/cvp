# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.dock_node import PASSTHRU_CENTRAL_NODE, DockNodeFlags
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import WindowFlags, merge_window_flags
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


def dock_space_over_viewport(
    dockspace_id: int = 0,
    viewport: Optional[imgui.Viewport] = None,
    dockspace_flags: Union[DockNodeFlags, int] = PASSTHRU_CENTRAL_NODE,
    window_class: Optional[imgui.WindowClass] = None,
    window_label: Optional[str] = None,
):
    if viewport is None:
        viewport = imgui.get_main_viewport()
    assert isinstance(viewport, imgui.Viewport)

    # Submit a window filling the entire viewport
    imgui.set_next_window_pos(viewport.work_pos, cond=0, pivot=None)
    imgui.set_next_window_size(viewport.work_size, cond=0)
    imgui.set_next_window_viewport(viewport.id_)

    host_window_flags = merge_window_flags(
        WindowFlags.none,
        WindowFlags.no_title_bar,
        WindowFlags.no_collapse,
        WindowFlags.no_resize,
        WindowFlags.no_move,
        WindowFlags.no_docking,
        WindowFlags.no_bring_to_front_on_focus,
        WindowFlags.no_nav_focus,
    )

    if dockspace_flags & DockNodeFlags.passthru_central_node:
        host_window_flags |= WindowFlags.no_background.value

    if window_label is None:
        window_label = f"WindowOverViewport_{viewport.id_:08X}"
    assert isinstance(window_label, str)

    imgui.push_style_var(StyleVar.window_rounding.value, 0.0)
    imgui.push_style_var(StyleVar.window_border_size.value, 0.0)
    imgui.push_style_var(StyleVar.window_padding.value, (0.0, 0.0))
    imgui.begin(window_label, None, host_window_flags)
    imgui.pop_style_var(3)

    # Submit the dockspace
    if dockspace_id == 0:
        dockspace_id = get_id("DockSpace")
    assert 1 <= dockspace_id

    imgui.dock_space(dockspace_id, (0.0, 0.0), dockspace_flags, window_class)

    imgui.end()

    return dockspace_id

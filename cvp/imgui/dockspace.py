# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui

from cvp.imgui.flags import dock_node


@contextmanager
def dockspace_context(name: str):
    # viewport = imgui.get_main_viewport()
    # imgui.set_next_window_pos(viewport.work_pos)
    # imgui.set_next_window_size(viewport.work_size)

    # imgui.begin(name, None, dock_node.DOCKSPACE_FLAGS)
    # imgui.dock_space(dock_space_id, None, dock_node.DOCKSPACE_FLAGS)

    dock_space_id = imgui.get_id(name)
    imgui.dock_space_over_viewport(
        dock_space_id,
        imgui.get_main_viewport(),
        dock_node.PASSTHRU_CENTRAL_NODE,
    )

    try:
        yield dock_space_id
    finally:
        imgui.end()

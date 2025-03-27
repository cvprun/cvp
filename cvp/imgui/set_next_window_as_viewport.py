# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def set_next_window_as_viewport() -> None:
    viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos(viewport.work_pos)
    imgui.set_next_window_size(viewport.work_size)

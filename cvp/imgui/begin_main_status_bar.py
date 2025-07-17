# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui

from cvp.imgui.flags.window import VIEWPORT_SIDE_BAR_FLAGS


def begin_main_status_viewport() -> bool:
    return imgui.internal.begin_viewport_side_bar(
        "##MainStatusBar",
        imgui.get_main_viewport(),
        imgui.Dir.down,
        imgui.get_frame_height(),
        VIEWPORT_SIDE_BAR_FLAGS,
    )


def end_main_status_viewport() -> None:
    imgui.end()


def begin_main_status_bar() -> bool:
    return imgui.begin_menu_bar()


def end_main_status_bar() -> None:
    imgui.end_menu_bar()


@contextmanager
def begin_main_status_bar_context():
    viewport_open = begin_main_status_viewport()
    assert viewport_open

    result = begin_main_status_bar()
    try:
        yield result
    finally:
        end_main_status_bar()
        end_main_status_viewport()

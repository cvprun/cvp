# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui


def begin_popup_context_window(
    label: Optional[str] = None,
    flags=1,
    also_over_items=True,
):
    return imgui.begin_popup_context_window(label, flags, also_over_items)


def end_popup_context_window() -> None:
    imgui.end_popup()

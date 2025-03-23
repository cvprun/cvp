# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui


def begin_popup_context_window(label: Optional[str] = None, flags=1):
    return imgui.begin_popup_context_window(label, flags)


def end_popup_context_window() -> None:
    imgui.end_popup()

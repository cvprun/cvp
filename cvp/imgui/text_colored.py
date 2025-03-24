# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def text_colored(text: str, color: imgui.ImVec4Like) -> None:
    imgui.text_colored(color, text)

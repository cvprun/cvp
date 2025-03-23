# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def begin_menu(label: str, enabled=True):
    return imgui.begin_menu(label, enabled)


def end_menu() -> None:
    imgui.end_menu()

# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui


def begin_menu_bar() -> bool:
    return imgui.begin_menu_bar()


def end_menu_bar() -> None:
    imgui.end_menu_bar()


@contextmanager
def begin_menu_bar_context():
    result = begin_menu_bar()
    try:
        yield result
    finally:
        end_menu_bar()

# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui


def begin_child(
    label: Union[str, int],
    width=0.0,
    height=0.0,
    border=False,
    flags=0,
):
    return imgui.begin_child(label, width, height, border, flags)  # noqa


def end_child() -> None:
    imgui.end_child()

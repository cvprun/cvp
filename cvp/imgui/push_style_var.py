# -*- coding: utf-8 -*-

from contextlib import contextmanager
from enum import StrEnum, unique
from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags import style_var


@unique
class DefaultStyles(StrEnum):
    """
    ImGui style names start with a capital letter.

    Do not use `enum.auto()` when assigning values, as it forces them to lowercase.
    """

    Dark = "Dark"
    Light = "Light"
    Classic = "Classic"


def style_colors(style: DefaultStyles) -> None:
    if style == DefaultStyles.Dark:
        imgui.style_colors_dark()
    elif style == DefaultStyles.Light:
        imgui.style_colors_light()
    elif style == DefaultStyles.Classic:
        imgui.style_colors_classic()
    else:
        raise ValueError(f"Unknown style: {style}")


def default_style_colors(
    style: Union[str, DefaultStyles],
    default=DefaultStyles.Dark,
) -> None:
    try:
        if not isinstance(style, DefaultStyles):
            style = DefaultStyles(style)
        style_colors(style)
    except:  # noqa
        style_colors(default)


@contextmanager
def style_window_padding_context(x: float, y: float):
    imgui.push_style_var(style_var.WINDOW_PADDING, (x, y))
    try:
        yield
    finally:
        imgui.pop_style_var()


@contextmanager
def style_item_spacing_context(x: float, y: float):
    imgui.push_style_var(style_var.ITEM_SPACING, (x, y))
    try:
        yield
    finally:
        imgui.pop_style_var()


@contextmanager
def style_frame_border_size_context(value: float):
    imgui.push_style_var(style_var.FRAME_BORDER_SIZE, value)
    try:
        yield
    finally:
        imgui.pop_style_var()

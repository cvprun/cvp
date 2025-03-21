# -*- coding: utf-8 -*-

from contextlib import contextmanager
from enum import StrEnum, unique
from typing import Final, Union

from imgui_bundle import imgui

from cvp.types.colors import RGBA


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
def style_window_padding(x: float, y: float):
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (x, y))
    try:
        yield
    finally:
        imgui.pop_style_var()


@contextmanager
def style_item_spacing(x: float, y: float):
    imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (x, y))
    try:
        yield
    finally:
        imgui.pop_style_var()


DEFAULT_DISABLE_TEXT_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 1.0
DEFAULT_DISABLE_BACKGROUND_COLOR: Final[RGBA] = 0.2, 0.2, 0.2, 1.0


@contextmanager
def style_disable_input(
    text_color=DEFAULT_DISABLE_TEXT_COLOR,
    background_color=DEFAULT_DISABLE_BACKGROUND_COLOR,
):
    imgui.push_style_color(imgui.COLOR_TEXT, *text_color)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *background_color)
    try:
        yield
    finally:
        imgui.pop_style_color(2)

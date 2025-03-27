# -*- coding: utf-8 -*-

from typing import Final, Sequence

from imgui_bundle import hello_imgui


def get_theme(index: int):
    return hello_imgui.ImGuiTheme_(index)


def get_theme_name(index: int) -> str:
    return get_theme(index).name


THEME_COUNT: Final[int] = int(hello_imgui.ImGuiTheme_.count.value)
THEME_NAMES: Final[Sequence[str]] = tuple(get_theme_name(i) for i in range(THEME_COUNT))

DEFAULT_THEME: Final[hello_imgui.ImGuiTheme_] = hello_imgui.ImGuiTheme_.darcula_darker
DEFAULT_THEME_NAME: Final[str] = DEFAULT_THEME.name


def apply_theme_with_index(index: int) -> None:
    if 0 <= index < THEME_COUNT:
        hello_imgui.apply_theme(hello_imgui.ImGuiTheme_(index))
    else:
        raise IndexError(f"Out of range theme index: {index}")

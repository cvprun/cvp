# -*- coding: utf-8 -*-

from typing import Any, Sequence, Union

from imgui_bundle import imgui

from cvp.palette import find_named_color

ColorLike = Union[int, str, Sequence[float]]


def validate_color_element(color: Sequence[Any], i: int) -> None:
    x = color[i]
    if not isinstance(x, float):
        raise TypeError(f"#{i} color element is not of float type: {type(x).__name__}")
    if not (0.0 <= x <= 1.0):
        raise ValueError(f"#{i} color element is not between 0.0 and 1.0: {x}")


def color_normalize_u32(color: ColorLike, *, validate=False) -> int:
    if isinstance(color, int):
        return color
    elif isinstance(color, str):
        rgb = find_named_color(color)
        if rgb is None:
            raise ValueError(f"Could not find named color: '{color}'")
        r, g, b = rgb
        return imgui.get_color_u32((r, g, b, 1.0))
    elif isinstance(color, Sequence):
        match len(color):
            case 3:
                if validate:
                    validate_color_element(color, 0)
                    validate_color_element(color, 1)
                    validate_color_element(color, 2)
                return imgui.get_color_u32((*color, 1.0))
            case 4:
                if validate:
                    validate_color_element(color, 0)
                    validate_color_element(color, 1)
                    validate_color_element(color, 2)
                    validate_color_element(color, 3)
                return imgui.get_color_u32((*color,))
            case _:
                raise ValueError("The number of color elements must be 3 or 4")
    else:
        raise TypeError(f"Unexpected color type: {type(color).__name__}")

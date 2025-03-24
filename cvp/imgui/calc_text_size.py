# -*- coding: utf-8 -*-

from typing import Optional, Tuple

from imgui_bundle import imgui


def calc_text_size(
    text: str,
    text_end: Optional[str] = None,
    hide_text_after_double_hash: bool = False,
    wrap_width: float = -1.0,
) -> Tuple[float, float]:
    size = imgui.calc_text_size(text, text_end, hide_text_after_double_hash, wrap_width)
    x, y = size.x, size.y
    assert isinstance(x, float)
    assert isinstance(y, float)
    return x, y

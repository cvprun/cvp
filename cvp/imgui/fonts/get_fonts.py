# -*- coding: utf-8 -*-

from typing import Tuple, Optional

from imgui_bundle import imgui
from numpy import ndarray, uint8
from numpy.typing import NDArray


def get_fonts() -> imgui.ImFontAtlas:
    return imgui.get_io().fonts


def get_tex_data_as_rgba32(fonts: Optional[imgui.ImFontAtlas] = None) -> NDArray[uint8]:
    if fonts is None:
        fonts = get_fonts()
    assert fonts is not None
    func = getattr(fonts, "get_tex_data_as_rgba32")
    assert func is not None
    assert callable(func)
    return func()


def get_tex_data_as_raw_rgba32(
    fonts: Optional[imgui.ImFontAtlas] = None,
) -> Tuple[int, int, bytes]:
    tex = get_tex_data_as_rgba32(fonts)
    assert isinstance(tex, ndarray)
    assert tex.dtype == uint8
    assert 3 == len(tex.shape)

    height, width, channels = tex.shape
    assert 0 < height
    assert 0 < width
    assert 4 == channels  # RGBA32 == 4bytes

    data = tex.tobytes()
    assert isinstance(data, bytes)
    assert height * width * channels == len(data)

    return width, height, data

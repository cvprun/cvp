# -*- coding: utf-8 -*-

from typing import Dict, NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.gl.textures.numpy import NumpyTexture
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.types.colors import RGBA
from cvp.types.shapes import Point


class AtlasItem(NamedTuple):
    uv_min: Point
    uv_max: Point


class BaseAtlas(Dict[str, AtlasItem]):
    def __init__(self):
        super().__init__()
        self._texture = NumpyTexture()

    @property
    def texture(self):
        return self._texture

    @property
    def opened(self) -> bool:
        return self._texture.opened

    def draw(
        self,
        key: str,
        p1: Point,
        p2: Point,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        *,
        draw_list: Optional[DrawList] = None,
    ) -> None:
        if not self._texture.opened:
            raise ValueError("Atlas is not opened")

        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None

        if not isinstance(color, (tuple, list)):
            color = imgui.get_color_u32(color)
        assert isinstance(color, int)

        texture_id = self._texture.texture_id
        draw_list = imgui.get_window_draw_list()
        item = self.__getitem__(key)
        uv_min = item.uv_min
        uv_max = item.uv_max
        draw_list.add_image(texture_id, p1, p2, uv_min, uv_max, color)

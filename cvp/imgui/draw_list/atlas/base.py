# -*- coding: utf-8 -*-

from typing import Dict, NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.gl.textures.numpy import NumpyTexture
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.types.colors import RGBA
from cvp.types.shapes import Point


class AtlasItem(NamedTuple):
    index_: int
    p1: Point
    p2: Point
    offset: Point
    uv_p1: Point
    uv_p2: Point
    ascent: int = 0
    descent: int = 0
    name: str = str()

    @property
    def x1(self):
        return self.p1[0]

    @property
    def y1(self):
        return self.p1[1]

    @property
    def x2(self):
        return self.p2[0]

    @property
    def y2(self):
        return self.p2[1]

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def size(self):
        return self.width, self.height

    @property
    def offset_x(self):
        return self.offset[0]

    @property
    def offset_y(self):
        return self.offset[1]


class BaseAtlas(Dict[int, AtlasItem]):
    def __init__(self):
        super().__init__()
        self._texture = NumpyTexture()

    @property
    def texture(self):
        return self._texture

    @property
    def opened(self) -> bool:
        return self._texture.opened

    @property
    def width(self):
        return self.texture.width

    @property
    def height(self):
        return self.texture.height

    @property
    def size(self):
        return self.texture.size

    def add_image_with_key(
        self,
        key: int,
        p1: Point,
        p2: Point,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        draw_list: Optional[DrawList] = None,
    ) -> None:
        item = self.__getitem__(key)
        self.add_image_with_item(item, p1, p2, color, draw_list)

    def add_image_with_item(
        self,
        item: AtlasItem,
        p1: Point,
        p2: Point,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        draw_list: Optional[DrawList] = None,
    ) -> None:
        if not self._texture.opened:
            raise ValueError("Texture is not opened")

        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None

        if not isinstance(color, (tuple, list)):
            color = imgui.get_color_u32(color)
        assert isinstance(color, int)

        texture_id = self._texture.texture_id
        draw_list = imgui.get_window_draw_list()
        x1 = p1[0] + item.offset_x
        y1 = p1[1] + item.offset_y
        x2 = p2[0] + item.offset_x
        y2 = p2[1] + item.offset_y
        p1 = x1, y1
        p2 = x2, y2
        draw_list.add_image(texture_id, p1, p2, item.uv_p1, item.uv_p2, color)

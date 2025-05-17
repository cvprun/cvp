# -*- coding: utf-8 -*-

from math import ceil, isqrt
from typing import Dict, Final, List, Optional, Tuple, Union

from imgui_bundle import imgui
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ranges import BlockRange
from cvp.fonts.ttf import TTF
from cvp.imgui.draw_list.atlas.base import AtlasItem, BaseAtlas
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.ttf.renderer import add_text_stroke
from cvp.imgui.draw_list.types import DrawList
from cvp.types.colors import RGBA
from cvp.types.shapes import Point
from cvp.variables import FONT_SIZE, UNICODE_SINGLE_BLOCK_SIZE


class FontAtlas(BaseAtlas):
    _ttf: Optional[TTF]
    _blocks: List[BlockRange]
    _codepoints: Dict[int, CodepointInfo]

    PILLOW_IMAGE_MODE: Final[str] = "RGBA"
    PILLOW_COLOR_TRANSPARENT: Final[Tuple[int, int, int, int]] = 0, 0, 0, 0
    PILLOW_COLOR_WHITE: Final[Tuple[int, int, int, int]] = 255, 255, 255, 255

    def __init__(self, block_size=UNICODE_SINGLE_BLOCK_SIZE):
        super().__init__()

        self._ttf = None
        self._blocks = list()
        self._codepoints = dict()
        self._font_size = 0

        self._block_size = block_size
        self._line_count = isqrt(block_size)

        if self._line_count**2 != self._block_size:
            raise ValueError("Block size must be square")

    @classmethod
    def new_pillow_image(cls, width: int, height: int):
        return Image.new(
            mode=cls.PILLOW_IMAGE_MODE,
            size=(width, height),
            color=cls.PILLOW_COLOR_TRANSPARENT,
        )

    def open(self, path: str, size=FONT_SIZE):
        if self.opened:
            raise ValueError("Font file already opened")

        ttf = TTF.from_filepath(path)
        pillow_font = truetype(path, size)
        blocks = ttf.get_block_ranges(self._block_size)
        chars = ttf.get_character_map()
        codepoints = dict()
        items: Dict[int, AtlasItem] = dict()

        cell_width = size
        cell_height = size
        cols = self._line_count
        rows = ceil(len(chars) / self._line_count)
        canvas_width = cell_width * cols
        canvas_height = cell_height * rows

        image = self.new_pillow_image(canvas_width, canvas_height)
        draw = Draw(image)

        for i, item in enumerate(chars.items()):
            item_col = i % cols
            item_row = i // cols

            x = item_col * cell_width
            y = item_row * cell_height
            pivot = x, y

            codepoint, glyph_name = item
            text = chr(codepoint)
            bbox = draw.textbbox(pivot, text, font=pillow_font)
            draw.text(pivot, text, self.PILLOW_COLOR_WHITE, font=pillow_font)
            ascent, descent = pillow_font.getmetrics()

            p1 = bbox[0], bbox[1]
            p2 = bbox[2], bbox[3]

            uv_min = bbox[0] / canvas_width, bbox[1] / canvas_height
            uv_max = bbox[2] / canvas_width, bbox[3] / canvas_height

            atlas = AtlasItem(p1, p2, uv_min, uv_max, ascent, descent, glyph_name)
            items[codepoint] = atlas
            codepoints[codepoint] = CodepointInfo(codepoint, ttf)

        assert not self._texture.opened
        assert 0 == self.__len__()
        self._texture.open_with_pillow(image)
        self._ttf = ttf
        self._blocks = blocks
        self._codepoints = codepoints
        self._font_size = size
        self.update(items)

    def close(self) -> None:
        if not self.opened:
            raise ValueError("Font file not opened")

        assert self._texture.opened
        self._texture.close()

        assert not self._texture.opened
        assert self._ttf is not None

        self._ttf.close()
        self._ttf = None
        self._blocks.clear()
        self._codepoints.clear()
        self._font_size = 0
        self.clear()

    @property
    def path(self) -> str:
        return str(self._ttf.path) if self._ttf is not None else str()

    @property
    def ttf(self):
        return self._ttf

    @property
    def blocks(self):
        return self._blocks

    @property
    def codepoints(self):
        return self._codepoints

    @property
    def font_size(self):
        return self._font_size

    @property
    def block_size(self):
        return self._block_size

    @property
    def line_count(self):
        return self._line_count

    def add_text_stroke(
        self,
        text: str,
        size: int,
        point: Point,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        draw_list: Optional[DrawList] = None,
    ) -> None:
        if not self.opened:
            raise ValueError("Font file not opened")

        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None
        assert self._ttf is not None

        add_text_stroke(
            self._ttf.ttfont,
            size,
            text,
            point,
            color,
            draw_list,
        )

    def add_text_atlas(
        self,
        text: str,
        point: Point,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        draw_list: Optional[DrawList] = None,
    ) -> None:
        if not self.opened:
            raise ValueError("Font file not opened")

        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None

        if isinstance(color, (tuple, list)):
            color = imgui.get_color_u32(color)
        assert isinstance(color, int)

        x = point[0]
        y = point[1]

        for c in text:
            item = self.__getitem__(ord(c))

            width = item.width
            height = item.height

            p1 = x, y
            p2 = x + width, y + height

            self.add_image_with_item(item, p1, p2, color, draw_list)
            x += width

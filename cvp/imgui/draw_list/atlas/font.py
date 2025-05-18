# -*- coding: utf-8 -*-

from math import ceil, isqrt
from typing import Callable, Final, Optional, Tuple, Union

from imgui_bundle import imgui
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ttf import TTF
from cvp.imgui.draw_list.atlas.base import AtlasItem, BaseAtlas
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.ttf.renderer import add_text_stroke
from cvp.imgui.draw_list.types import DrawList
from cvp.types.colors import RGBA
from cvp.types.shapes import Point
from cvp.variables import FONT_SIZE, UNICODE_SINGLE_BLOCK_SIZE


class FontAtlasLoader:
    """
    Since the font atlas relies on an OpenGL texture, and OpenGL restricts texture
    creation to the main thread, the processes of loading glyphs and initializing
    textures should be handled separately.
    """

    PILLOW_IMAGE_MODE: Final[str] = "RGBA"
    PILLOW_COLOR_TRANSPARENT: Final[Tuple[int, int, int, int]] = 0, 0, 0, 0
    PILLOW_COLOR_WHITE: Final[Tuple[int, int, int, int]] = 255, 255, 255, 255

    def __init__(
        self,
        path: str,
        size=FONT_SIZE,
        block_size=UNICODE_SINGLE_BLOCK_SIZE,
        padding_size=1,
        *,
        callback: Optional[Callable[[int, int], None]] = None,
    ):
        self.font_size = size
        self.block_size = block_size
        self.line_count = isqrt(block_size)
        self.padding_size = padding_size

        if self.line_count**2 != self.block_size:
            raise ValueError("Block size must be square")

        self.ttf = TTF.from_filepath(path)
        self.pillow_font = truetype(path, self.font_size)
        self.blocks = self.ttf.get_block_ranges(self.block_size)
        self.chars = self.ttf.get_character_map()
        self.codepoints = dict()
        self.atlas_items = dict()
        self.family = self.ttf.font_family_name
        self.subfamily = self.ttf.font_subfamily_name
        self.is_monospace = self.ttf.is_monospace

        max_chars = len(self.chars)
        cols = self.line_count
        rows = ceil(max_chars / self.line_count)

        cell_width = self.font_size
        cell_height = self.font_size

        canvas_width = cell_width * cols
        canvas_height = cell_height * rows

        self.image = Image.new(
            mode=self.PILLOW_IMAGE_MODE,
            size=(canvas_width, canvas_height),
            color=self.PILLOW_COLOR_TRANSPARENT,
        )
        draw = Draw(self.image)
        ascent, descent = self.pillow_font.getmetrics()

        next_x = 0
        next_y = 0
        line_max_height = 0.0

        for i, item in enumerate(self.chars.items()):
            # =============================
            # item_col = i % cols
            # item_row = i // cols
            # x1 = item_col * cell_width
            # y1 = item_row * cell_height
            # -----------------------------
            x1 = next_x
            y1 = next_y
            # =============================

            p1 = x1, y1

            codepoint, glyph_name = item
            text = chr(codepoint)

            bbox = draw.textbbox(p1, text, font=self.pillow_font)
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]
            assert y1 + bbox_height < canvas_height

            if x1 + bbox_width < canvas_width:
                line_max_height = max(line_max_height, bbox_height)
                next_x += bbox_width + self.padding_size
            else:
                assert canvas_width <= x1 + bbox_width
                # Too wide for canvas, draw on next line.

                next_x = bbox_width + self.padding_size
                next_y += line_max_height + self.padding_size
                line_max_height = bbox_height

                x1 = 0
                y1 = next_y
                p1 = x1, y1

                bbox = draw.textbbox(p1, text, font=self.pillow_font)
                bbox_width = bbox[2] - bbox[0]
                bbox_height = bbox[3] - bbox[1]

                assert x1 + bbox_width < canvas_width
                assert y1 + bbox_height < canvas_height

            x2 = x1 + bbox_width
            y2 = y1 + bbox_height
            p2 = x2, y2

            offset_x = bbox[0] - x1
            offset_y = bbox[1] - y1
            offset = offset_x, offset_y

            draw_x = x1 - offset_x
            draw_y = y1 - offset_y
            draw_point = draw_x, draw_y
            draw.text(draw_point, text, self.PILLOW_COLOR_WHITE, font=self.pillow_font)

            uv_min = x1 / canvas_width, y1 / canvas_height
            uv_max = x2 / canvas_width, y2 / canvas_height

            atlas = AtlasItem(
                index_=i,
                p1=p1,
                p2=p2,
                offset=offset,
                uv_p1=uv_min,
                uv_p2=uv_max,
                ascent=ascent,
                descent=descent,
                name=glyph_name,
            )

            self.atlas_items[codepoint] = atlas
            self.codepoints[codepoint] = CodepointInfo(codepoint, self.ttf)

            if callback is not None:
                callback(i, max_chars)

    def close(self) -> None:
        self.atlas_items.clear()
        self.codepoints.clear()
        self.blocks.clear()
        self.ttf.close()
        self.image.close()


class FontAtlas(BaseAtlas):
    _loader: Optional[FontAtlasLoader]

    def __init__(self):
        super().__init__()
        self._loader = None

    def open(
        self,
        path: str,
        size=FONT_SIZE,
        block_size=UNICODE_SINGLE_BLOCK_SIZE,
        *,
        callback: Optional[Callable[[int, int], None]] = None,
    ):
        if self._texture.opened:
            raise ValueError("Font file already opened")

        loader = FontAtlasLoader(path, size, block_size, callback=callback)
        self.open_with_loader(loader)

    def open_with_loader(self, loader: FontAtlasLoader):
        if self._texture.opened:
            raise ValueError("Font file already opened")

        self._loader = loader
        self._texture.open_with_pillow(loader.image)
        self.update(loader.atlas_items)

    def close(self) -> None:
        if not self._texture.opened:
            assert self._loader is None
            raise ValueError("Font file not opened")

        assert self._texture.opened
        assert self._loader is not None
        self.clear()
        self._texture.close()
        self._loader.close()
        self._loader = None

    @property
    def path(self) -> str:
        return str(self._loader.ttf.path) if self._loader else str()

    @property
    def ttf(self):
        return self._loader.ttf if self._loader else None

    @property
    def blocks(self):
        return self._loader.blocks if self._loader else list()

    @property
    def codepoints(self):
        return self._loader.codepoints if self._loader else dict()

    @property
    def font_size(self):
        return self._loader.font_size if self._loader else 0

    @property
    def block_size(self):
        return self._loader.block_size if self._loader else 0

    @property
    def line_count(self):
        return self._loader.line_count if self._loader else 0

    @property
    def family(self) -> str:
        return self._loader.family if self._loader else str()

    @property
    def subfamily(self) -> str:
        return self._loader.subfamily if self._loader else str()

    @property
    def is_monospace(self) -> str:
        return self._loader.is_monospace if self._loader else str()

    @property
    def spacing_type(self) -> str:
        return "Monospace" if self.is_monospace else "Proportional"

    def __repr__(self):
        return (
            f"<{type(self).__name__}"
            f" {self.family}"
            f",{self.subfamily}"
            f",{self.font_size}px"
            ">"
        )

    def __str__(self):
        return f"{self.family}, {self.subfamily}, {self.font_size}, {self.spacing_type}"

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

        add_text_stroke(
            self.ttf.ttfont,
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

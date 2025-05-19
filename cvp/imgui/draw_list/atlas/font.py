# -*- coding: utf-8 -*-

from io import BytesIO
from math import ceil
from os import PathLike
from typing import BinaryIO, Callable, Final, Optional, Tuple, Union

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
from cvp.pillow.crop_to_content import crop_bottom_to_content
from cvp.types.colors import RGBA
from cvp.types.shapes import Point, Size
from cvp.variables import DEFAULT_MAX_TEXTURE_SIZE, FONT_SIZE, UNICODE_SINGLE_BLOCK_SIZE


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
        file: Union[str, PathLike[str], BinaryIO],
        size=FONT_SIZE,
        block_size=UNICODE_SINGLE_BLOCK_SIZE,
        max_texture_size=DEFAULT_MAX_TEXTURE_SIZE,
        padding_pixels=1,
        *,
        callback: Optional[Callable[[int, int], None]] = None,
    ):
        self.font_size = size
        self.block_per_items = block_size
        self.padding_pixels = padding_pixels

        self.ttf = TTF.from_file(file)
        self.pillow_font = truetype(BytesIO(self.ttf.as_bytes()), self.font_size)
        self.blocks = self.ttf.get_block_ranges(self.block_per_items)
        self.chars = self.ttf.get_character_map()
        self.codepoints = dict()
        self.atlas_items = dict()
        self.family = self.ttf.font_family_name
        self.subfamily = self.ttf.font_subfamily_name
        self.is_monospace = self.ttf.is_monospace
        self.is_variable = self.ttf.is_variable

        ascent, descent = self.pillow_font.getmetrics()
        assert 0 < ascent
        assert 0 < descent
        cell_height = abs(ascent) + abs(descent)
        cell_width = self.font_size

        max_chars = len(self.chars)
        cols = max_texture_size / cell_width
        rows = ceil(max_chars / cols)

        canvas_width = max_texture_size
        canvas_height = cell_height * rows

        self.image = Image.new(
            mode=self.PILLOW_IMAGE_MODE,
            size=(canvas_width, canvas_height),
            color=self.PILLOW_COLOR_TRANSPARENT,
        )
        draw = Draw(self.image)

        next_x = 0.0
        next_y = 0.0
        line_max_height = 0.0

        for i, item in enumerate(self.chars.items()):
            x1 = next_x
            y1 = next_y

            p1 = x1, y1

            codepoint, glyph_name = item
            text = chr(codepoint)

            bbox = draw.textbbox(p1, text, font=self.pillow_font)
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]

            if canvas_height <= y1 + bbox_height:
                extra_h = ceil(max(1.0, (max_chars - i) / cols) * cell_height * 2)
                canvas_height += extra_h
                new_image = Image.new(
                    mode=self.PILLOW_IMAGE_MODE,
                    size=(canvas_width, canvas_height),
                    color=self.PILLOW_COLOR_TRANSPARENT,
                )
                draw = Draw(new_image)
                new_image.paste(self.image, (0, 0))
                self.image = new_image

            if x1 + bbox_width < canvas_width:
                line_max_height = max(line_max_height, bbox_height)
                next_x += bbox_width + self.padding_pixels
            else:
                assert canvas_width <= x1 + bbox_width
                # Too wide for canvas, draw on next line.

                next_x = bbox_width + self.padding_pixels
                next_y += line_max_height + self.padding_pixels
                line_max_height = bbox_height

                x1 = 0.0
                y1 = next_y
                p1 = x1, y1

                bbox = draw.textbbox(p1, text, font=self.pillow_font)
                bbox_width = bbox[2] - bbox[0]
                bbox_height = bbox[3] - bbox[1]

                assert x1 + bbox_width < canvas_width

                if canvas_height <= y1 + bbox_height:
                    extra_h = ceil(max(1.0, (max_chars - i) / cols) * cell_height * 2)
                    canvas_height += extra_h
                    new_image = Image.new(
                        mode=self.PILLOW_IMAGE_MODE,
                        size=(canvas_width, canvas_height),
                        color=self.PILLOW_COLOR_TRANSPARENT,
                    )
                    draw = Draw(new_image)
                    new_image.paste(self.image, (0, 0))
                    self.image = new_image

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

            # [IMPORTANT]
            # Since the UV coordinates change when the canvas size changes,
            # we calculate them all at once at the end.
            # uv_p1 = x1 / canvas_width, y1 / canvas_height
            # uv_p2 = x2 / canvas_width, y2 / canvas_height
            uv_p1 = 0.0, 0.0
            uv_p2 = 0.0, 0.0

            atlas = AtlasItem(
                index_=i,
                p1=p1,
                p2=p2,
                offset=offset,
                uv_p1=uv_p1,
                uv_p2=uv_p2,
                ascent=ascent,
                descent=descent,
                name=glyph_name,
            )

            self.atlas_items[codepoint] = atlas
            self.codepoints[codepoint] = CodepointInfo(codepoint, self.ttf)

            if callback is not None:
                callback(i, max_chars)

        self.image = crop_bottom_to_content(self.image)

        # Recalculate the UV coordinates based on the most recently updated canvas size.
        canvas_width = self.image.width
        canvas_height = self.image.height
        for codepoint in self.atlas_items.keys():
            old_atlas = self.atlas_items[codepoint]
            x1, y1 = old_atlas.p1
            x2, y2 = old_atlas.p2
            uv_p1 = x1 / canvas_width, y1 / canvas_height
            uv_p2 = x2 / canvas_width, y2 / canvas_height
            new_atlas = AtlasItem(
                index_=old_atlas.index_,
                p1=old_atlas.p1,
                p2=old_atlas.p2,
                offset=old_atlas.offset,
                uv_p1=uv_p1,
                uv_p2=uv_p2,
                ascent=old_atlas.ascent,
                descent=old_atlas.descent,
                name=old_atlas.name,
            )
            self.atlas_items[codepoint] = new_atlas

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
        file: Union[str, PathLike[str], BinaryIO],
        size=FONT_SIZE,
        block_size=UNICODE_SINGLE_BLOCK_SIZE,
        *,
        callback: Optional[Callable[[int, int], None]] = None,
    ):
        if self._texture.opened:
            raise ValueError("Font file already opened")

        loader = FontAtlasLoader(file, size, block_size, callback=callback)
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
        return self._loader.block_per_items if self._loader else 0

    @property
    def family(self) -> str:
        return self._loader.family if self._loader else str()

    @property
    def subfamily(self) -> str:
        return self._loader.subfamily if self._loader else str()

    @property
    def is_variable(self) -> bool:
        return self._loader.is_variable if self._loader else False

    @property
    def is_monospace(self) -> bool:
        return self._loader.is_monospace if self._loader else False

    def __repr__(self):
        return (
            f"<{type(self).__name__}"
            f" {self.family}"
            f",{self.subfamily}"
            f",{self.font_size}px"
            ">"
        )

    def __str__(self):
        return f"{self.family}, {self.subfamily}, {self.font_size}"

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
    ) -> Size:
        if not self.opened:
            raise ValueError("Font file not opened")

        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None

        if isinstance(color, (tuple, list)):
            color = imgui.get_color_u32(color)
        assert isinstance(color, int)

        ascent = self.ttf.ascent or 0
        descent = self.ttf.descent or 0
        line_gap = self.ttf.line_gap or 0
        assert ascent is not None
        assert descent is not None
        assert line_gap is not None

        line_height = abs(ascent) + abs(descent) + abs(line_gap)

        x1 = point[0]
        y1 = point[1]

        cursor_x = x1
        cursor_y = y1

        for c in text:
            try:
                item = self.__getitem__(ord(c))
            except KeyError:
                continue

            width = item.width
            height = item.height

            p1 = cursor_x, cursor_y
            p2 = cursor_x + width, cursor_y + height

            self.add_image_with_item(item, p1, p2, color, draw_list)
            cursor_x += width

        return cursor_x - point[0], cursor_y + line_height

    def text_colored(self, text: str, color: Union[int, RGBA] = 0xFFFFFFFF) -> None:
        if isinstance(color, (tuple, list)):
            color = imgui.get_color_u32(color)
        assert isinstance(color, int)

        draw_list = get_window_draw_list()
        screen_pos = imgui.get_cursor_screen_pos()
        cx, cy = screen_pos.x, screen_pos.y

        size = self.add_text_atlas(text, (cx, cy), color, draw_list)
        imgui.dummy(size)

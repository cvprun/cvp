# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, Optional, Union

from imgui_bundle import imgui

from cvp.fonts.cached_ttf import CachedTTF
from cvp.fonts.ranges import UNICODE_SINGLE_BLOCK_SIZE, BlockRange, CodepointRange
from cvp.fonts.ttf import TTF
from cvp.gl.textures.texture import Texture
from cvp.imgui.fonts.font import Font
from cvp.imgui.fonts.get_fonts import get_tex_data_as_raw_rgba32
from cvp.imgui.fonts.glyph_ranges import create_glyph_ranges


class FontBuilder:
    _font: Optional[imgui.ImFont]
    _ttfs: List[CachedTTF]

    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

        self._font = None
        self._ttfs = list()

        self._merge = imgui.ImFontConfig()
        self._merge.merge_mode = True

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def fonts(self):
        return imgui.get_io().fonts

    def add_ttf(
        self,
        path: Union[str, PathLike[str]],
        ranges: Optional[List[CodepointRange]] = None,
        *,
        size: Optional[int] = None,
    ):
        ttf = TTF.from_filepath(path)

        if not ranges:
            ranges = ttf.get_glyph_ranges()

        if not size:
            size = self._size

        if not ranges:
            raise ValueError("Invalid ranges")
        if not size:
            raise ValueError("Invalid size")
        if size < 0:
            raise ValueError("Invalid size")

        fonts = imgui.get_io().fonts
        filename = str(ttf.path)
        config = None if self._font is None else self._merge
        glyph_ranges = create_glyph_ranges(ranges)
        self._font = fonts.add_font_from_file_ttf(filename, size, config, glyph_ranges)
        self._ttfs.append(CachedTTF(ttf, ranges, size))
        return self

    @staticmethod
    def _create_font_texture() -> Texture:
        fonts = imgui.get_io().fonts

        width, height, pixels = get_tex_data_as_raw_rgba32(fonts)

        texture = Texture()
        texture.open(width, height)
        with texture:
            texture.update_alpha_pixels(pixels)
        return texture

    def _create_blocks(self, step=UNICODE_SINGLE_BLOCK_SIZE) -> List[BlockRange]:
        result = set()
        for ttf in self._ttfs:
            for cp_range in ttf.ranges:
                for block_range in cp_range.as_blocks(step):
                    result.add(block_range)
        return list(sorted(result, key=lambda x: x[0]))

    def done(self, block_step=UNICODE_SINGLE_BLOCK_SIZE, *, use_texture=False) -> Font:
        if self._font is None:
            raise ValueError("No font was created")

        return Font(
            self._font,
            self._name,
            self._size,
            block_step,
            self._ttfs,
            self._create_blocks(block_step),
            self._create_font_texture() if use_texture else None,
        )

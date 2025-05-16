# -*- coding: utf-8 -*-

from math import isqrt
from typing import Dict, List, Optional

from PIL.ImageFont import FreeTypeFont, truetype

from cvp.fonts.codepoint_info import CodepointInfo
from cvp.fonts.ranges import BlockRange
from cvp.fonts.ttf import TTF
from cvp.imgui.draw_list.atlas.base import BaseAtlas
from cvp.variables import FONT_SIZE, UNICODE_SINGLE_BLOCK_SIZE


class FontAtlas(BaseAtlas):
    _ttf: Optional[TTF]
    _pillow_font: Optional[FreeTypeFont]
    _blocks: List[BlockRange]
    _codepoints: Dict[int, CodepointInfo]

    def __init__(self, block_size=UNICODE_SINGLE_BLOCK_SIZE):
        super().__init__()
        self._ttf = None
        self._pillow_font = None
        self._blocks = list()
        self._codepoints = dict()
        self._block_size = block_size

    def open(self, path: str, size=FONT_SIZE):
        if self._texture.opened:
            self._texture.close()
            self._pillow_font = None

        assert not self._texture.opened
        line_count = isqrt(self._block_size)
        width = size * line_count
        height = 100000

        ttf = TTF.from_filepath(path)
        self._blocks = ttf.get_block_ranges(self._block_size)
        self._pillow_font = truetype(path, size)
        self._texture.open_with_empty(width, height, channels=1)

    def close(self) -> None:
        if self._texture.opened:
            self._texture.close()

        assert not self._texture.opened
        self._pillow_font = None
        self._blocks.clear()
        self._codepoints.clear()

    @property
    def path(self) -> str:
        return str(self._ttf.path) if self._ttf is not None else str()

    @property
    def ttf(self):
        assert self._ttf is not None
        return self._ttf.ttf

    def get_codepoint_info(self, codepoint: int) -> CodepointInfo:
        info = self._codepoints.get(codepoint)
        if info is None:
            info = CodepointInfo(codepoint, self._ttf)
            self._codepoints[codepoint] = info
        return info

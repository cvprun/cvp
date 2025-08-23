# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from cvp.colors.convert.imgui import argb8888_to_uint32


@dataclass
class SgrGlyph:
    row: int
    col: int

    char: Optional[str] = None

    foreground: Union[None, int, Tuple[int, int, int]] = None
    background: Union[None, int, Tuple[int, int, int]] = None

    error: Optional[str] = None

    @property
    def pos(self) -> Tuple[int, int]:
        return self.row, self.col

    @property
    def background_u32(self) -> Optional[int]:
        if self.background is None:
            return None

        if isinstance(self.background, int):
            return self.background

        assert isinstance(self.background, tuple)
        assert 3 == len(self.background)

        r, g, b = self.background
        return argb8888_to_uint32(255, r, g, b)

    @property
    def foreground_u32(self) -> Optional[int]:
        if self.foreground is None:
            return None

        if isinstance(self.foreground, int):
            return self.foreground

        assert isinstance(self.foreground, tuple)
        assert 3 == len(self.foreground)

        r, g, b = self.foreground
        return argb8888_to_uint32(255, r, g, b)

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union

from cvp.colors.convert.imgui import argb8888_to_uint32


@dataclass
class TerminalStyle:
    bold: bool = False
    faint: bool = False  # Dim
    italic: bool = False
    underline: bool = False
    blink_speed: int = 0
    inverse: bool = False
    hide: bool = False  # Conceal
    strike: bool = False  # Crossed-out

    font: Optional[int] = None

    foreground: Union[None, int, Tuple[int, int, int]] = None
    background: Union[None, int, Tuple[int, int, int]] = None

    underline_color: Union[None, int, Tuple[int, int, int]] = None

    def reset(self):
        self.bold = False
        self.faint = False
        self.italic = False
        self.underline = False
        self.blink_speed = 0
        self.inverse = False
        self.hide = False
        self.strike = False
        self.font = None
        self.foreground = None
        self.background = None
        self.underline_color = None

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

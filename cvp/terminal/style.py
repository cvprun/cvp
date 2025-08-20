# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union


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

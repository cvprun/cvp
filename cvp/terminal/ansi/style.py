# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Tuple, Union


@dataclass
class TerminalStyle:
    bold: bool = False
    faint: bool = False
    italic: bool = False
    underline: bool = False
    slow_blink: bool = False
    rapid_blink: bool = False
    inverse: bool = False
    hide: bool = False
    strike: bool = False

    foreground: Union[None, int, Tuple[int, int, int]] = None
    background: Union[None, int, Tuple[int, int, int]] = None

    def reset(self):
        self.bold = False
        self.faint = False
        self.italic = False
        self.underline = False
        self.slow_blink = False
        self.rapid_blink = False
        self.inverse = False
        self.hide = False
        self.strike = False
        self.foreground = None
        self.background = None

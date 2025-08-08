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

    foreground: Union[int, Tuple[int, int, int]] = 0
    background: Union[int, Tuple[int, int, int]] = 0

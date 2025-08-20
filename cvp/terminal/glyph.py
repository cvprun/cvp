# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union


@dataclass
class TerminalGlyph:
    row: int
    col: int

    char: Optional[str] = None

    foreground: Union[None, int, Tuple[int, int, int]] = None
    background: Union[None, int, Tuple[int, int, int]] = None

    error: Optional[str] = None

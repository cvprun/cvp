# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union


@dataclass
class TerminalGlyph:
    char: str
    row: int
    col: int

    foreground: Union[None, int, Tuple[int, int, int]] = None
    background: Union[None, int, Tuple[int, int, int]] = None

    error: Optional[str] = None

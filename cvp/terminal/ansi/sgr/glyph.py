# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Tuple, Union


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

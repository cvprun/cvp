# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.config.sections.bases.window import WindowConfig

DEFAULT_BOARD_ROWS: Final[int] = 20
DEFAULT_BOARD_COLS: Final[int] = 10
DEFAULT_CELL_PIXELS: Final[int] = 20


@dataclass
class GlyphHackWindowConfig(WindowConfig):
    board_rows: int = DEFAULT_BOARD_ROWS
    board_cols: int = DEFAULT_BOARD_COLS
    cell_pixels: int = DEFAULT_CELL_PIXELS
    slot_index: int = 0

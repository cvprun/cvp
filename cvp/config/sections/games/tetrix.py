# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.palette.basic import FUCHSIA, RED, WHITE
from cvp.types.colors import RGB

DEFAULT_BOARD_ROWS: Final[int] = 20
DEFAULT_BOARD_COLS: Final[int] = 10
DEFAULT_CELL_PIXELS: Final[int] = 20
DEFAULT_DROP_INTERVAL_INIT: Final[float] = 0.5
DEFAULT_DROP_INTERVAL_STEP: Final[float] = 0.1


@dataclass
class TetrixConfig:
    board_rows: int = DEFAULT_BOARD_ROWS
    board_cols: int = DEFAULT_BOARD_COLS
    cell_pixels: int = DEFAULT_CELL_PIXELS
    drop_interval_init: float = DEFAULT_DROP_INTERVAL_INIT
    drop_interval_step: float = DEFAULT_DROP_INTERVAL_STEP
    current_block_color: RGB = FUCHSIA
    fixed_block_color: RGB = RED
    outline_color: RGB = WHITE
    high_score: int = 0

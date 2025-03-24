# -*- coding: utf-8 -*-

from typing import Tuple

import numpy as np
from imgui_bundle import imgui

from cvp.config.sections.games.glyph_hack import (
    DEFAULT_BOARD_COLS,
    DEFAULT_BOARD_ROWS,
    DEFAULT_CELL_PIXELS,
    GlyphHackWindowConfig,
)
from cvp.imgui.button import button
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override


class GlyphHackWindow(WindowBase[GlyphHackWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.glyph_hack_window,
            title="Glyph Hack",
            closable=True,
            flags=None,
            modifiable_title=False,
        )

        config = context.config.glyph_hack_window
        assert DEFAULT_BOARD_ROWS <= config.board_rows
        assert DEFAULT_BOARD_COLS <= config.board_cols
        assert DEFAULT_CELL_PIXELS <= config.cell_pixels

        rows = config.board_rows
        cols = config.board_cols
        self._board = np.zeros((rows, cols), dtype=int)
        self._game_over = True

    @property
    def window_padding(self) -> Tuple[float, float]:
        padding = imgui.get_style().window_padding
        return padding.x, padding.y

    @property
    def cell_pixels(self):
        return self.window_config.cell_pixels

    @property
    def cols(self):
        return self._board.shape[1]

    @property
    def rows(self):
        return self._board.shape[0]

    def get_cell(self, x: int, y: int) -> int:
        return self._board[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self._board[y][x] = value

    def clear_board(self) -> None:
        rows = self.window_config.tetrix_window.board_rows
        cols = self.window_config.tetrix_window.board_cols
        self._board = np.zeros((rows, cols), dtype=int)

    def clear_state(self) -> None:
        self._board = np.zeros((self.rows, self.cols), dtype=int)
        self._game_over = True

    @override
    def on_process(self) -> None:
        imgui.text("Glyphos")

        if button("Start", disabled=not self._game_over):
            self._game_over = False
        imgui.same_line()
        if button("Stop", disabled=self._game_over):
            self._game_over = True
        imgui.separator()

        if self._game_over:
            text_centered("Game Over")
            return

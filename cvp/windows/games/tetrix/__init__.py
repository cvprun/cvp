# -*- coding: utf-8 -*-

from random import choice
from typing import Final, Sequence, Tuple

import imgui
import numpy as np

from cvp.config.sections.games.tetrix import (
    DEFAULT_BOARD_COLS,
    DEFAULT_BOARD_ROWS,
    DEFAULT_CELL_PIXELS,
    DEFAULT_DROP_INTERVAL_INIT,
    DEFAULT_DROP_INTERVAL_STEP,
    TetrixWindowConfig,
)
from cvp.imgui.button import button
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override
from cvp.types.shapes import Rect

SINGLE_LINE_CLEAR_SCORE: Final[int] = 100
DOUBLE_LINE_CLEAR_SCORE: Final[int] = 300
TRIPLE_LINE_CLEAR_SCORE: Final[int] = 500
TETRIX_LINE_CLEAR_SCORE: Final[int] = 800
LINE_CLEAR_SCORES: Final[Sequence[int]] = (
    SINGLE_LINE_CLEAR_SCORE,
    DOUBLE_LINE_CLEAR_SCORE,
    TRIPLE_LINE_CLEAR_SCORE,
    TETRIX_LINE_CLEAR_SCORE,
)

T_SPIN_SCORE: Final[int] = 800
T_SPIN_SINGLE_SCORE: Final[int] = 800
T_SPIN_DOUBLE_SCORE: Final[int] = 1200
T_SPIN_TRIPLE_SCORE: Final[int] = 1600

BlockShapeType = Sequence[Sequence[int]]

BLOCK_I: Final[BlockShapeType] = ((1, 1, 1, 1),)
BLOCK_O: Final[BlockShapeType] = ((1, 1), (1, 1))
BLOCK_T: Final[BlockShapeType] = ((1, 1, 1), (0, 1, 0))
BLOCK_L: Final[BlockShapeType] = ((1, 1, 1), (1, 0, 0))
BLOCK_LR: Final[BlockShapeType] = ((1, 1, 1), (0, 0, 1))
BLOCK_S: Final[BlockShapeType] = ((1, 1, 0), (0, 1, 1))
BLOCK_SR: Final[BlockShapeType] = ((0, 1, 1), (1, 1, 0))

BLOCKS: Final[Sequence[BlockShapeType]] = (
    BLOCK_I,
    BLOCK_O,
    BLOCK_T,
    BLOCK_L,
    BLOCK_LR,
    BLOCK_S,
    BLOCK_SR,
)


class TetrixWindow(WindowBase[TetrixWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.tetrix_window,
            title="TetriX",
            closable=True,
            flags=None,
            modifiable_title=False,
        )

        config = context.config.tetrix_window
        assert DEFAULT_BOARD_ROWS <= config.board_rows
        assert DEFAULT_BOARD_COLS <= config.board_cols
        assert DEFAULT_CELL_PIXELS <= config.cell_pixels
        assert DEFAULT_DROP_INTERVAL_INIT <= config.drop_interval_init
        assert DEFAULT_DROP_INTERVAL_STEP <= config.drop_interval_step

        rows = config.board_rows
        cols = config.board_cols
        self._board = np.zeros((rows, cols), dtype=int)

        self._blocks = BLOCKS
        self._current_block = self._blocks[0]
        self._current_pos = [0, 0]
        self._game_over = True
        self._current_score = 0
        self._current_time = 0.0
        self._last_drop_time = 0.0
        self._drop_interval = config.drop_interval_init
        self.new_piece()

    @property
    def window_padding(self) -> Tuple[int, int]:
        return imgui.get_style().window_padding

    @property
    def cell_pixels(self):
        return self.window_config.cell_pixels

    @property
    def current_y(self):
        return self._current_pos[0]

    @current_y.setter
    def current_y(self, value: int) -> None:
        self._current_pos[0] = value

    @property
    def current_x(self):
        return self._current_pos[1]

    @current_x.setter
    def current_x(self, value: int) -> None:
        self._current_pos[1] = value

    @property
    def current_block_color(self):
        return imgui.get_color_u32_rgba(*self.window_config.current_block_color, 1.0)

    @property
    def fixed_block_color(self):
        return imgui.get_color_u32_rgba(*self.window_config.fixed_block_color, 1.0)

    @property
    def outline_color(self):
        return imgui.get_color_u32_rgba(*self.window_config.outline_color, 1.0)

    @property
    def high_score(self):
        return self.window_config.high_score

    @high_score.setter
    def high_score(self, value: int) -> None:
        self.window_config.high_score = value

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
        self._current_pos = [0, 0]
        self._game_over = True
        self._current_score = 0
        self._current_time = 0.0
        self._last_drop_time = 0.0
        self.new_piece()

    def new_piece(self):
        self._current_block = choice(BLOCKS)
        self._current_pos = [0, self.cols // 2 - len(self._current_block[0]) // 2]

        if not self.is_valid_move(0, 0):
            self._game_over = True
            if self.high_score < self._current_score:
                self.high_score = self._current_score

    def is_valid_move(self, dy: int, dx: int):
        for y, row in enumerate(self._current_block):
            for x, cell in enumerate(row):
                if not cell:
                    continue

                new_y = self.current_y + y + dy
                new_x = self.current_x + x + dx

                if (
                    new_y >= self.rows
                    or new_x < 0
                    or new_x >= self.cols
                    or (new_y >= 0 and self.get_cell(new_x, new_y))
                ):
                    return False

        return True

    def move(self, dx: int) -> None:
        if self._game_over:
            return
        if not self.is_valid_move(0, dx):
            return
        self._current_pos[1] += dx

    def rotate(self):
        if not self._game_over:
            rotated = list(zip(*self._current_block[::-1]))
            original_piece = self._current_block
            self._current_block = rotated

            if not self.is_valid_move(0, 0):
                self._current_block = original_piece

    def soft_drop(self):
        if not self._game_over and self.is_valid_move(1, 0):
            self._current_pos[0] += 1
        else:
            self.lock_piece()
            self.clear_lines()
            self.new_piece()

    def hard_drop(self):
        pass

    def lock_piece(self):
        for y, row in enumerate(self._current_block):
            for x, cell in enumerate(row):
                if cell:
                    ny = self._current_pos[0] + y
                    nx = self._current_pos[1] + x
                    if 0 <= ny < self.rows and 0 <= nx < self.cols:
                        self._board[ny][nx] = 1

    def clear_lines(self):
        lines_cleared = 0
        y = self.rows - 1
        while y >= 0:
            if all(self._board[y]):
                self._board = np.delete(self._board, y, axis=0)
                self._board = np.vstack([np.zeros(self.cols, dtype=int), self._board])
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared > 0:
            self._current_score += [0, 40, 100, 300, 1200][lines_cleared]

    @override
    def on_process(self) -> None:
        imgui.text(f"Score: {self._current_score}")
        imgui.same_line()
        imgui.text(f"High: {self.high_score}")

        if button("Start", disabled=not self._game_over):
            self._current_score = 0
            self._board[::] = 0
            self._game_over = False
            self._current_pos = [0, 0]
        imgui.same_line()
        if button("Stop", disabled=self._game_over):
            if self.high_score < self._current_score:
                self.high_score = self._current_score
            self._game_over = True
        imgui.separator()

        if self._game_over:
            text_centered("Game Over")
            return

        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()
        assert isinstance(cx, float)
        assert isinstance(cy, float)
        assert isinstance(cw, float)
        assert isinstance(ch, float)

        canvas_roi = cx, cy, cx + cw, cy + ch
        draw_list = get_window_draw_list()

        self.process_auto_drop()
        self.process_key_events()
        self.draw_bord(draw_list, canvas_roi)
        self.draw_current_block(draw_list, canvas_roi)

    def process_auto_drop(self) -> None:
        self._current_time = imgui.get_time()
        if self._current_time - self._last_drop_time > self._drop_interval:
            self.soft_drop()
            self._last_drop_time = self._current_time

    def process_key_events(self) -> None:
        kmap = imgui.get_io().key_map
        if imgui.is_key_pressed(kmap[imgui.KEY_LEFT_ARROW]):
            self.move(-1)
        if imgui.is_key_pressed(kmap[imgui.KEY_RIGHT_ARROW]):
            self.move(1)
        if imgui.is_key_pressed(kmap[imgui.KEY_DOWN_ARROW]):
            self.soft_drop()
        if imgui.is_key_pressed(kmap[imgui.KEY_UP_ARROW]):
            self.rotate()
        if imgui.is_key_pressed(kmap[imgui.KEY_SPACE]):
            self.hard_drop()

    def draw_bord(self, draw_list: DrawList, canvas_roi: Rect) -> None:
        fixed_block_color = self.fixed_block_color
        outline_color = self.outline_color
        cx = canvas_roi[0] + self.window_padding[0]
        cy = canvas_roi[1] + self.window_padding[1]
        cell_pixels = self.cell_pixels

        for y in range(self.rows):
            for x in range(self.cols):
                x1 = cx + x * cell_pixels
                y1 = cy + y * cell_pixels
                x2 = x1 + cell_pixels
                y2 = y1 + cell_pixels

                if self.get_cell(x, y):
                    draw_list.add_rect_filled(x1, y1, x2, y2, fixed_block_color)

                draw_list.add_rect(x1, y1, x2, y2, outline_color)

    def draw_current_block(self, draw_list: DrawList, canvas_roi: Rect) -> None:
        if self._game_over:
            return

        block_color = self.current_block_color
        cx = canvas_roi[0] + self.window_padding[0]
        cy = canvas_roi[1] + self.window_padding[1]
        cell_pixels = self.cell_pixels
        current_x = self.current_x
        current_y = self.current_y

        for y, row in enumerate(self._current_block):
            for x, cell in enumerate(row):
                if not cell:
                    continue

                x1 = cx + (current_x + x) * cell_pixels
                y1 = cy + (current_y + y) * cell_pixels
                x2 = x1 + cell_pixels
                y2 = y1 + cell_pixels

                draw_list.add_rect_filled(x1, y1, x2, y2, block_color)

# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui
from pygame import SYSTEM_CURSOR_SIZENS, SYSTEM_CURSOR_SIZEWE
from pygame.cursors import Cursor
from pygame.mouse import get_cursor, set_cursor

from cvp.imgui.splitter import (
    AVAILABLE_REGION_SIZE,
    DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER,
    DEFAULT_SPLITTER_SIZE,
    DEFAULT_SPLITTER_THICKNESS,
    DEFAULT_VERTICAL_SPLITTER_IDENTIFIER,
    SplitterOrientation,
    SplitterResult,
    splitter,
)
from cvp.logging.loggers import widgets_logger as logger
from cvp.patterns.proxy import ValueProxy


class Splitter:
    _hovered_cursor: Optional[Cursor]
    _prev_cursor: Optional[Cursor]

    def __init__(
        self,
        identifier: str,
        orientation: SplitterOrientation,
        width: float,
        height: float,
        value_proxy: Optional[ValueProxy[float]] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        negative_delta=False,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = None,
    ):
        self._identifier = identifier
        self._orientation = orientation
        self._width = width
        self._height = height
        self._store = value_proxy
        self._min_value = float(min_value) if min_value is not None else None
        self._max_value = float(max_value) if max_value is not None else None
        self._negative_delta = negative_delta
        self._flags = flags
        self._thickness = thickness

        self._hovered_cursor = None
        self._prev_cursor = None
        self._prev_hovered = False
        self._moving = False

        self._pivot_value = 0.0
        self._delta_charger = 0.0

        if cursor is not None:
            if isinstance(cursor, Cursor):
                self._hovered_cursor = cursor
            elif isinstance(cursor, int):
                self._hovered_cursor = Cursor(cursor)
            else:
                raise TypeError(f"Unsupported cursor type: {type(cursor).__name__}")

    def __repr__(self):
        return (
            f"<{type(self).__name__}"
            f" moving={self._moving}"
            f" store={self._store.get() if self._store else None}"
            f" pivot={self._pivot_value:.3f}"
            f" delta={self._delta_charger:.3f}"
            ">"
        )

    @classmethod
    def from_vertical(
        cls,
        identifier=DEFAULT_VERTICAL_SPLITTER_IDENTIFIER,
        width=DEFAULT_SPLITTER_SIZE,
        height=AVAILABLE_REGION_SIZE,
        value_proxy: Optional[ValueProxy[float]] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        negative_delta=False,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZEWE,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.vertical,
            width=width,
            height=height,
            value_proxy=value_proxy,
            min_value=min_value,
            max_value=max_value,
            negative_delta=negative_delta,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    @classmethod
    def from_horizontal(
        cls,
        identifier=DEFAULT_HORIZONTAL_SPLITTER_IDENTIFIER,
        width=AVAILABLE_REGION_SIZE,
        height=DEFAULT_SPLITTER_SIZE,
        value_proxy: Optional[ValueProxy[float]] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        negative_delta=False,
        flags=0,
        thickness=DEFAULT_SPLITTER_THICKNESS,
        cursor: Optional[Union[Cursor, int]] = SYSTEM_CURSOR_SIZENS,
    ):
        return cls(
            identifier=identifier,
            orientation=SplitterOrientation.horizontal,
            width=width,
            height=height,
            value_proxy=value_proxy,
            min_value=min_value,
            max_value=max_value,
            negative_delta=negative_delta,
            flags=flags,
            thickness=thickness,
            cursor=cursor,
        )

    @property
    def moving(self) -> bool:
        return self._moving

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    def get_mouse_value(self) -> float:
        match self._orientation:
            case SplitterOrientation.vertical:
                return imgui.get_io().mouse_pos.x
            case SplitterOrientation.horizontal:
                return imgui.get_io().mouse_pos.y
            case _:
                assert False, "Inaccessible Section"

    def change_hovered_cursor(self) -> None:
        if self._hovered_cursor is None:
            return

        self._prev_cursor = get_cursor()
        set_cursor(self._hovered_cursor)

    def change_prev_cursor(self) -> None:
        if self._prev_cursor is None:
            return

        set_cursor(self._prev_cursor)
        self._prev_cursor = None

    def on_start_moving(self) -> None:
        if self._store is not None:
            self._pivot_value = self._store.get()
        self._delta_charger = 0.0

    def on_end_moving(self) -> None:
        pass

    def normalize_value(self, value: float):
        if self._min_value is not None:
            if value < self._min_value:
                return self._min_value

        if self._max_value is not None:
            if value > self._max_value:
                return self._max_value

        return value

    def next_store_value(self, result: SplitterResult) -> float:
        assert self._store is not None
        assert result.changed

        delta = (-1 if self._negative_delta else 1) * self._delta_charger
        value = self._pivot_value + delta
        return self.normalize_value(value)

    def do_splitter(self):
        return splitter(
            self._identifier,
            self._orientation,
            self._width,
            self._height,
            self._flags,
            self._thickness,
        )

    def do_process(self):
        result = self.do_splitter()

        # Update cursor
        if not self._prev_hovered and result.hovered:
            self.change_hovered_cursor()
            self._prev_hovered = True
        elif self._prev_hovered and not result.hovered and not result.changed:
            self.change_prev_cursor()
            self._prev_hovered = False

        # Update moving
        if not self._moving and result.changed:
            self._moving = True
            self.on_start_moving()
        elif self._moving and not result.changed:
            self._moving = False
            self.on_end_moving()

        if result.changed:
            self._delta_charger += result.value
            if self._store is not None:
                self._store.set(self.next_store_value(result))

        if self._moving:
            logger.debug(repr(self))

        return result

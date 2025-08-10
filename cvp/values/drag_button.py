# -*- coding: utf-8 -*-

from enum import Enum, auto, unique
from typing import Optional

from cvp.types.shapes import Point
from cvp.values.delta import DeltaValue


@unique
class DragState(Enum):
    normal = auto()
    ready = auto()
    dragging = auto()


class DragButton:
    def __init__(self, state=DragState.normal, pivot: Optional[Point] = None) -> None:
        self._down = DeltaValue.from_single_value(False)
        self._drag = DeltaValue.from_single_value(False)
        self._state = state
        self._pivot = pivot

    @property
    def down(self):
        return self._down

    @property
    def drag(self):
        return self._drag

    @property
    def state(self):
        return self._state

    @property
    def pivot(self):
        return self._pivot

    @property
    def is_down(self) -> bool:
        return self._down.value

    @property
    def is_up(self) -> bool:
        return not self._down.value

    @property
    def changed_down(self) -> bool:
        return self._down.changed and self._down.value

    @property
    def changed_up(self) -> bool:
        return self._down.changed and not self._down.value

    @property
    def is_dragging(self) -> bool:
        return self._drag.value

    @property
    def start_drag(self) -> bool:
        return self._drag.changed and self._drag.value

    @property
    def end_drag(self) -> bool:
        return self._drag.changed and not self._drag.value

    def update(self, down: bool, point: Point) -> None:
        if self._down.update(down):
            if self._down.value:
                self._state = DragState.ready
                self._pivot = point
            else:
                self._state = DragState.normal
                self._pivot = None

        if not self._down.value:
            assert self._state == DragState.normal
            assert self._pivot is None
            self._drag.update(False)
            return

        assert self._state != DragState.normal
        assert self._pivot is not None

        if self._state == DragState.ready and self._pivot != point:
            self._state = DragState.dragging

        self._drag.update(self._state == DragState.dragging)

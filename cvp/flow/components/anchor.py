# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.shapes import Point


@dataclass
class Anchor:
    x: float = 0.0
    y: float = 0.0

    _selected: bool = False
    _hovering: bool = False

    @property
    def point(self):
        return self.x, self.y

    @point.setter
    def point(self, value: Point) -> None:
        self.x = value[0]
        self.y = value[1]

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value

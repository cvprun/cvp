# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

from cvp.canvas.axis import Axis
from cvp.canvas.control import ViewControl
from cvp.canvas.grid import Grid
from cvp.canvas.pixel import Pixel
from cvp.canvas.options import DrawingOptions
from cvp.types.colors import BLACK_RGBA, RGBA

CanvasKey = NewType("CanvasKey", str)


@dataclass
class CanvasProps:
    pixel: Pixel = field(default_factory=Pixel)

    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)

    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)

    control: ViewControl = field(default_factory=ViewControl)
    options: DrawingOptions = field(default_factory=DrawingOptions)

    background_color: RGBA = BLACK_RGBA


@dataclass
class CanvasWindow:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    workspace: str = field(default_factory=str)
    name: str = field(default_factory=str)
    opened: bool = False

    @property
    def key(self):
        return CanvasKey(self.uuid)

    @key.setter
    def key(self, value: CanvasKey) -> None:
        self.uuid = str(value)


@dataclass
class Canvas(CanvasProps, CanvasWindow):
    pass

# -*- coding: utf-8 -*-

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Optional

from cvp.pins.action import Action
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size


@dataclass
class FlowPin:
    name: str = str()
    docs: str = str()
    dtype: str = str()
    action: Action = Action.data
    stream: Stream = Stream.input
    required: bool = False
    arcs: List[str] = field(default_factory=list)

    icon_pos: Point = EMPTY_POINT
    icon_size: Size = EMPTY_SIZE

    name_pos: Point = EMPTY_POINT
    name_size: Size = EMPTY_SIZE

    _selected: bool = False
    _hovering: bool = False
    _connectable: bool = False

    _template: Optional[Pin] = None

    @classmethod
    def from_template(cls, template: Pin):
        return cls(
            name=template.name,
            docs=template.docs,
            dtype=template.dtype,
            action=template.action,
            stream=template.stream,
            required=template.required,
            arcs=deepcopy(template.arcs),
            _template=template,
        )

    @property
    def template(self):
        return self._template

    @property
    def is_data_action(self):
        return self.action == Action.data

    @property
    def is_flow_action(self):
        return self.action == Action.flow

    @property
    def is_input_stream(self):
        return self.stream == Stream.input

    @property
    def is_output_stream(self):
        return self.stream == Stream.output

    @property
    def is_flow_inputs(self) -> bool:
        return self.is_flow_action and self.is_input_stream

    @property
    def is_flow_outputs(self) -> bool:
        return self.is_flow_action and self.is_output_stream

    @property
    def is_data_inputs(self) -> bool:
        return self.is_data_action and self.is_input_stream

    @property
    def is_data_outputs(self) -> bool:
        return self.is_data_action and self.is_output_stream

    @property
    def connected(self) -> bool:
        return bool(self.arcs)

    @property
    def icon_roi(self) -> Rect:
        x, y = self.icon_pos
        w, h = self.icon_size
        return x, y, x + w, y + h

    @icon_roi.setter
    def icon_roi(self, value: Rect) -> None:
        x1, y1, x2, y2 = value
        self.icon_pos = x1, y1
        self.icon_size = x2 - x1, y2 - y1

    @property
    def name_roi(self) -> Rect:
        x, y = self.name_pos
        w, h = self.name_size
        return x, y, x + w, y + h

    @name_roi.setter
    def name_roi(self, value: Rect) -> None:
        x1, y1, x2, y2 = value
        self.name_pos = x1, y1
        self.name_size = x2 - x1, y2 - y1

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

    @property
    def connectable(self):
        return self._connectable

    @connectable.setter
    def connectable(self, value: bool) -> None:
        self._connectable = value

    def as_unformatted_text(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Docs: {self.docs}\n"
            f"Data Type: {self.dtype}\n"
            f"Action: {self.action}\n"
            f"Stream: {self.stream}\n"
            f"Required: {self.required}\n"
            f"Arcs: {len(self.arcs)}\n"
            f"Icon pos: {self.icon_pos[0]:.02f}, {self.icon_pos[1]:.02f}\n"
            f"Icon size: {self.icon_size[0]:.02f}, {self.icon_size[1]:.02f}\n"
            f"Name pos: {self.name_pos[0]:.02f}, {self.name_pos[1]:.02f}\n"
            f"Name size: {self.name_size[0]:.02f}, {self.name_size[1]:.02f}\n"
            f"Selected: {self._selected}\n"
            f"Hovering: {self._hovering}\n"
            f"Connectable: {self._connectable}\n"
        )

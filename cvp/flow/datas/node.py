# -*- coding: utf-8 -*-

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

from cvp.flow.datas.pin import Pin
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size


@dataclass
class Node:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()
    icon: str = str()
    color: RGBA = WHITE_RGBA

    flow_inputs: List[Pin] = field(default_factory=list)
    flow_outputs: List[Pin] = field(default_factory=list)

    data_inputs: List[Pin] = field(default_factory=list)
    data_outputs: List[Pin] = field(default_factory=list)

    tags: List[str] = field(default_factory=list)

    head_height: float = 0.0
    flow_height: float = 0.0
    data_height: float = 0.0

    icon_pos: Point = EMPTY_POINT
    icon_size: Size = EMPTY_SIZE

    name_pos: Point = EMPTY_POINT
    name_size: Size = EMPTY_SIZE

    node_pos: Point = EMPTY_POINT
    node_size: Size = EMPTY_SIZE

    _selected: bool = False
    _hovering: bool = False

    @classmethod
    def from_template(cls, template: NodeTemplate):
        return cls(
            name=template.name,
            docs=template.docs,
            icon=template.icon,
            color=template.color,
            flow_inputs=list(Pin.from_template(p) for p in template.flow_inputs),
            flow_outputs=list(Pin.from_template(p) for p in template.flow_outputs),
            data_inputs=list(Pin.from_template(p) for p in template.data_inputs),
            data_outputs=list(Pin.from_template(p) for p in template.data_outputs),
            tags=deepcopy(template.tags),
        )

    def as_template(self):
        return NodeTemplate(
            name=self.name,
            docs=self.docs,
            icon=self.icon,
            color=self.color,
            pins=list(p.as_template() for p in self.pins),
            tags=deepcopy(self.tags),
        )

    def as_unformatted_text(self) -> str:
        return (
            f"Icon pos: {self.icon_pos[0]:.02f}, {self.icon_pos[1]:.02f}\n"
            f"Icon size: {self.icon_size[0]:.02f}, {self.icon_size[1]:.02f}\n"
            f"Name pos: {self.name_pos[0]:.02f}, {self.name_pos[1]:.02f}\n"
            f"Name size: {self.name_size[0]:.02f}, {self.name_size[1]:.02f}\n"
            f"Node pos: {self.node_pos[0]:.02f}, {self.node_pos[1]:.02f}\n"
            f"Node size: {self.node_size[0]:.02f}, {self.node_size[1]:.02f}\n"
        )

    @property
    def node_roi(self) -> Rect:
        x, y = self.node_pos
        w, h = self.node_size
        return x, y, x + w, y + h

    @node_roi.setter
    def node_roi(self, value: Rect) -> None:
        x1, y1, x2, y2 = value
        self.node_pos = x1, y1
        self.node_size = x2 - x1, y2 - y1

    @property
    def x1(self) -> float:
        return self.node_pos[0]

    @property
    def y1(self) -> float:
        return self.node_pos[1]

    @property
    def width(self) -> float:
        return self.node_size[0]

    @property
    def height(self) -> float:
        return self.node_size[1]

    @property
    def x2(self) -> float:
        return self.x1 + self.width

    @property
    def y2(self) -> float:
        return self.y1 + self.height

    @property
    def flow_pins(self) -> List[Pin]:
        return self.flow_inputs + self.flow_outputs

    @property
    def data_pins(self) -> List[Pin]:
        return self.data_inputs + self.data_outputs

    @property
    def input_pins(self) -> List[Pin]:
        return self.flow_inputs + self.data_inputs

    @property
    def output_pins(self) -> List[Pin]:
        return self.flow_outputs + self.data_outputs

    @property
    def pins(self) -> List[Pin]:
        return self.flow_pins + self.data_pins

    @property
    def flow_lines(self):
        return max(len(self.flow_inputs), len(self.flow_outputs))

    @property
    def data_lines(self):
        return max(len(self.data_inputs), len(self.data_outputs))

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

    def find_hovering_pin_with_mouse(self, mouse: Point) -> Optional[Pin]:
        mx, my = mouse
        for pin in self.pins:
            icon_x1 = self.node_pos[0] + pin.icon_pos[0]
            icon_y1 = self.node_pos[1] + pin.icon_pos[1]
            icon_w = pin.icon_size[0]
            icon_h = pin.icon_size[1]
            icon_x2 = icon_x1 + icon_w
            icon_y2 = icon_y1 + icon_h

            left = min(icon_x1, icon_x2)
            right = max(icon_x1, icon_x2)
            top = min(icon_y1, icon_y2)
            bottom = max(icon_y1, icon_y2)

            if left <= mx <= right and top <= my <= bottom:
                return pin
        return None

    def find_hovering_pin(self) -> Optional[Pin]:
        for pin in self.pins:
            if pin.hovering:
                return pin
        return None

    def find_selected_pins(self) -> List[Pin]:
        result = list()
        for pin in self.pins:
            if pin.selected:
                result.append(pin)
        return result

    def find_output_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.output_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

    def find_input_pin(self, arc_uuid: str) -> Optional[Pin]:
        for pin in self.input_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

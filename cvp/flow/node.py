# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Optional, Sequence
from uuid import uuid4

from type_serialize import Serializable, deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.pin import FlowPin
from cvp.nodes.node import Node
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size


@unique
class FlowNodeKeys(StrEnum):
    uuid = auto()
    name_ = "name"
    path = auto()
    docs = auto()
    icon = auto()
    lock = auto()
    breakpoint = auto()
    hidden = auto()
    color = auto()
    flow_inputs = auto()
    flow_outputs = auto()
    data_inputs = auto()
    data_outputs = auto()
    tags = auto()
    head_height = auto()
    flow_height = auto()
    data_height = auto()
    icon_pos = auto()
    icon_size = auto()
    name_pos = auto()
    name_size = auto()
    node_pos = auto()
    node_size = auto()


class FlowNode(Serializable):
    Keys = FlowNodeKeys

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        lock=False,
        breakpoint=False,
        hidden=False,
        color: RGBA = WHITE_RGBA,
        flow_inputs: Optional[Sequence[FlowPin]] = None,
        flow_outputs: Optional[Sequence[FlowPin]] = None,
        data_inputs: Optional[Sequence[FlowPin]] = None,
        data_outputs: Optional[Sequence[FlowPin]] = None,
        tags: Optional[Sequence[str]] = None,
        head_height=0.0,
        flow_height=0.0,
        data_height=0.0,
        icon_pos: Point = EMPTY_POINT,
        icon_size: Size = EMPTY_SIZE,
        name_pos: Point = EMPTY_POINT,
        name_size: Size = EMPTY_SIZE,
        node_pos: Point = EMPTY_POINT,
        node_size: Size = EMPTY_SIZE,
        *,
        selected: bool = False,
        hovering: bool = False,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.path = path if path else str()
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.lock = lock
        self.breakpoint = breakpoint
        self.hidden = hidden
        self.color = color

        self.flow_inputs = list(flow_inputs if flow_inputs else ())
        self.flow_outputs = list(flow_outputs if flow_outputs else ())
        self.data_inputs = list(data_inputs if data_inputs else ())
        self.data_outputs = list(data_outputs if data_outputs else ())
        self.tags = list(tags if tags else ())

        self.head_height = head_height
        self.flow_height = flow_height
        self.data_height = data_height

        self.icon_pos = icon_pos
        self.icon_size = icon_size
        self.name_pos = name_pos
        self.name_size = name_size
        self.node_pos = node_pos
        self.node_size = node_size

        self._selected = selected
        self._hovering = hovering

    @classmethod
    def from_template(cls, template: Node):
        return cls(
            uuid=str(uuid4()),
            name=template.name,
            path=template.path,
            docs=template.docs,
            icon=template.icon,
            lock=False,
            breakpoint=False,
            hidden=False,
            color=template.color,
            flow_inputs=list(FlowPin.from_template(p) for p in template.flow_inputs),
            flow_outputs=list(FlowPin.from_template(p) for p in template.flow_outputs),
            data_inputs=list(FlowPin.from_template(p) for p in template.data_inputs),
            data_outputs=list(FlowPin.from_template(p) for p in template.data_outputs),
            tags=deepcopy(template.tags),
        )

    def __str__(self) -> str:
        """In `cvp.flow` module, this return value is used as a key value."""
        return self.uuid

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False

        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.path == other.path
            and self.docs == other.docs
            and self.icon == other.icon
            and self.lock == other.lock
            and self.breakpoint == other.breakpoint
            and self.hidden == other.hidden
            and self.color == other.color
            and self.flow_inputs == other.flow_inputs
            and self.flow_outputs == other.flow_outputs
            and self.data_inputs == other.data_inputs
            and self.data_outputs == other.data_outputs
            and self.tags == other.tags
            and self.head_height == other.head_height
            and self.flow_height == other.flow_height
            and self.data_height == other.data_height
            and self.icon_pos == other.icon_pos
            and self.icon_size == other.icon_size
            and self.name_pos == other.name_pos
            and self.name_size == other.name_size
            and self.node_pos == other.node_pos
            and self.node_size == other.node_size
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.path = copy(self.path)
        result.docs = copy(self.docs)
        result.icon = copy(self.icon)
        result.lock = copy(self.lock)
        result.breakpoint = copy(self.breakpoint)
        result.hidden = copy(self.hidden)
        result.color = copy(self.color)
        result.flow_inputs = copy(self.flow_inputs)
        result.flow_outputs = copy(self.flow_outputs)
        result.data_inputs = copy(self.data_inputs)
        result.data_outputs = copy(self.data_outputs)
        result.tags = copy(self.tags)
        result.head_height = copy(self.head_height)
        result.flow_height = copy(self.flow_height)
        result.data_height = copy(self.data_height)
        result.icon_pos = copy(self.icon_pos)
        result.icon_size = copy(self.icon_size)
        result.name_pos = copy(self.name_pos)
        result.name_size = copy(self.name_size)
        result.node_pos = copy(self.node_pos)
        result.node_size = copy(self.node_size)
        result._selected = copy(self._selected)
        result._hovering = copy(self._hovering)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.path = deepcopy(self.path, memo)
        result.docs = deepcopy(self.docs, memo)
        result.icon = deepcopy(self.icon, memo)
        result.lock = deepcopy(self.lock, memo)
        result.breakpoint = deepcopy(self.breakpoint, memo)
        result.hidden = deepcopy(self.hidden, memo)
        result.color = deepcopy(self.color, memo)
        result.flow_inputs = deepcopy(self.flow_inputs, memo)
        result.flow_outputs = deepcopy(self.flow_outputs, memo)
        result.data_inputs = deepcopy(self.data_inputs, memo)
        result.data_outputs = deepcopy(self.data_outputs, memo)
        result.tags = deepcopy(self.tags, memo)
        result.head_height = deepcopy(self.head_height, memo)
        result.flow_height = deepcopy(self.flow_height, memo)
        result.data_height = deepcopy(self.data_height, memo)
        result.icon_pos = deepcopy(self.icon_pos, memo)
        result.icon_size = deepcopy(self.icon_size, memo)
        result.name_pos = deepcopy(self.name_pos, memo)
        result.name_size = deepcopy(self.name_size, memo)
        result.node_pos = deepcopy(self.node_pos, memo)
        result.node_size = deepcopy(self.node_size, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self.Keys.uuid: self.uuid,
            self.Keys.name_: self.name,
            self.Keys.path: self.path,
            self.Keys.docs: self.docs,
            self.Keys.icon: self.icon,
            self.Keys.lock: self.lock,
            self.Keys.breakpoint: self.breakpoint,
            self.Keys.hidden: self.hidden,
            self.Keys.color: list(self.color),
            self.Keys.flow_inputs: serialize(self.flow_inputs),
            self.Keys.flow_outputs: serialize(self.flow_outputs),
            self.Keys.data_inputs: serialize(self.data_inputs),
            self.Keys.data_outputs: serialize(self.data_outputs),
            self.Keys.tags: self.tags,
            self.Keys.head_height: self.head_height,
            self.Keys.flow_height: self.flow_height,
            self.Keys.data_height: self.data_height,
            self.Keys.icon_pos: list(self.icon_pos),
            self.Keys.icon_size: list(self.icon_size),
            self.Keys.name_pos: list(self.name_pos),
            self.Keys.name_size: list(self.name_size),
            self.Keys.node_pos: list(self.node_pos),
            self.Keys.node_size: list(self.node_size),
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = data.get(self.Keys.uuid, str())
        self.name = data.get(self.Keys.name_, str())
        self.path = data.get(self.Keys.path, str())
        self.docs = data.get(self.Keys.docs, str())
        self.icon = data.get(self.Keys.icon, str())
        self.lock = data.get(self.Keys.lock, False)
        self.breakpoint = data.get(self.Keys.breakpoint, False)
        self.hidden = data.get(self.Keys.hidden, False)

        self.color = tuple(data.get(self.Keys.color, WHITE_RGBA))
        assert len(self.color) == 4

        self.flow_inputs = list()
        self.flow_outputs = list()
        self.data_inputs = list()
        self.data_outputs = list()

        if flow_inputs := data.get(self.Keys.flow_inputs):
            for pin in flow_inputs:
                self.flow_inputs.append(deserialize(pin, FlowPin))
        if flow_outputs := data.get(self.Keys.flow_outputs):
            for pin in flow_outputs:
                self.flow_outputs.append(deserialize(pin, FlowPin))
        if data_inputs := data.get(self.Keys.data_inputs):
            for pin in data_inputs:
                self.data_inputs.append(deserialize(pin, FlowPin))
        if data_outputs := data.get(self.Keys.data_outputs):
            for pin in data_outputs:
                self.data_outputs.append(deserialize(pin, FlowPin))

        self.tags = data.get(self.Keys.tags, list())

        self.head_height = data.get(self.Keys.head_height, 0.0)
        self.flow_height = data.get(self.Keys.flow_height, 0.0)
        self.data_height = data.get(self.Keys.data_height, 0.0)

        self.icon_pos = tuple(data.get(self.Keys.icon_pos, EMPTY_POINT))
        self.icon_size = tuple(data.get(self.Keys.icon_size, EMPTY_SIZE))
        self.name_pos = tuple(data.get(self.Keys.name_pos, EMPTY_POINT))
        self.name_size = tuple(data.get(self.Keys.name_size, EMPTY_SIZE))
        self.node_pos = tuple(data.get(self.Keys.node_pos, EMPTY_POINT))
        self.node_size = tuple(data.get(self.Keys.node_size, EMPTY_SIZE))

        assert len(self.icon_pos) == 2
        assert len(self.icon_size) == 2
        assert len(self.name_pos) == 2
        assert len(self.name_size) == 2
        assert len(self.node_pos) == 2
        assert len(self.node_size) == 2

        self._selected = False
        self._hovering = False

    @property
    def as_flow_input_names(self):
        return [pin.name for pin in self.flow_inputs]

    @property
    def as_flow_output_names(self):
        return [pin.name for pin in self.flow_outputs]

    @property
    def as_data_input_names(self):
        return [pin.name for pin in self.data_inputs]

    @property
    def as_data_output_names(self):
        return [pin.name for pin in self.data_outputs]

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
    def flow_pins(self) -> List[FlowPin]:
        return self.flow_inputs + self.flow_outputs

    @property
    def data_pins(self) -> List[FlowPin]:
        return self.data_inputs + self.data_outputs

    @property
    def input_pins(self) -> List[FlowPin]:
        return self.flow_inputs + self.data_inputs

    @property
    def output_pins(self) -> List[FlowPin]:
        return self.flow_outputs + self.data_outputs

    @property
    def pins(self) -> List[FlowPin]:
        return self.flow_pins + self.data_pins

    @property
    def flow_lines(self):
        return max(len(self.flow_inputs), len(self.flow_outputs))

    @property
    def data_lines(self):
        return max(len(self.data_inputs), len(self.data_outputs))

    @property
    def has_flow_input(self) -> bool:
        return bool(self.flow_inputs)

    @property
    def has_flow_output(self) -> bool:
        return bool(self.flow_outputs)

    @property
    def is_begin(self) -> bool:
        return not self.has_flow_input and self.has_flow_output

    @property
    def is_middle(self) -> bool:
        return self.has_flow_input and self.has_flow_output

    @property
    def is_end(self) -> bool:
        return self.has_flow_input and not self.has_flow_output

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

    def as_unformatted_text(self) -> str:
        return (
            f"Uuid: {self.uuid}\n"
            f"Name: {self.name}\n"
            f"Docs: {self.docs}\n"
            f"Icon: {self.icon}\n"
            f"Lock: {self.lock}\n"
            f"Color: {self.color}\n"
            f"Flow inputs: {len(self.flow_inputs)}\n"
            f"Flow outputs: {len(self.flow_outputs)}\n"
            f"Data inputs: {len(self.data_inputs)}\n"
            f"Data outputs: {len(self.data_inputs)}\n"
            f"Begin: {self.is_begin}\n"
            f"Middle: {self.is_middle}\n"
            f"End: {self.is_end}\n"
            f"Tags: {self.tags}\n"
            f"Head height: {self.head_height:.02f}\n"
            f"Flow height: {self.flow_height:.02f}\n"
            f"Data height: {self.data_height:.02f}\n"
            f"Icon pos: {self.icon_pos[0]:.02f}, {self.icon_pos[1]:.02f}\n"
            f"Icon size: {self.icon_size[0]:.02f}, {self.icon_size[1]:.02f}\n"
            f"Name pos: {self.name_pos[0]:.02f}, {self.name_pos[1]:.02f}\n"
            f"Name size: {self.name_size[0]:.02f}, {self.name_size[1]:.02f}\n"
            f"Node pos: {self.node_pos[0]:.02f}, {self.node_pos[1]:.02f}\n"
            f"Node size: {self.node_size[0]:.02f}, {self.node_size[1]:.02f}\n"
            f"Selected: {self._selected}\n"
            f"Hovering: {self._hovering}\n"
        )

    def find_hovering_pin_with_mouse(self, mouse: Point) -> Optional[FlowPin]:
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

    def find_pin(self, pin_name: str) -> Optional[FlowPin]:
        for pin in self.pins:
            if pin.name == pin_name:
                return pin
        return None

    def find_hovering_pin(self) -> Optional[FlowPin]:
        for pin in self.pins:
            if pin.hovering:
                return pin
        return None

    def find_selected_pins(self) -> List[FlowPin]:
        result = list()
        for pin in self.pins:
            if pin.selected:
                result.append(pin)
        return result

    def find_output_pin(self, arc_uuid: str) -> Optional[FlowPin]:
        for pin in self.output_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

    def find_input_pin(self, arc_uuid: str) -> Optional[FlowPin]:
        for pin in self.input_pins:
            if arc_uuid in pin.arcs:
                return pin
        return None

    def remove_arc_from_pins(self, arc_uuid: str) -> None:
        for pin in self.pins:
            try:
                pin.arcs.remove(arc_uuid)
            except ValueError:
                pass

    def get_default(self, pin_name: str) -> Any:
        pin = self.find_pin(pin_name)
        if pin is None:
            raise KeyError(f"Not found pin: '{pin_name}'")
        return pin.default

    def set_default(self, pin_name: str, default: Any) -> None:
        pin = self.find_pin(pin_name)
        if pin is None:
            raise KeyError(f"Not found pin: '{pin_name}'")
        pin.default = default

    def get_dtype(self, pin_name: str) -> Dtype:
        pin = self.find_pin(pin_name)
        if pin is None:
            raise KeyError(f"Not found pin: '{pin_name}'")
        return pin.dtype

    def set_dtype(self, pin_name: str, dtype: Dtype) -> None:
        pin = self.find_pin(pin_name)
        if pin is None:
            raise KeyError(f"Not found pin: '{pin_name}'")
        pin.dtype = dtype

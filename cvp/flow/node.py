# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Iterable, List, NewType, Optional, Union
from uuid import uuid4

from type_serialize import Serializable, deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.pin import FlowPin
from cvp.flow.pins import FlowPins
from cvp.fonts.types import IconCode
from cvp.nodes.template import NodeName, NodePath, NodeTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size

NodeKey = NewType("NodeKey", str)


class FlowNode(Serializable):

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"
        path = auto()
        docs = auto()
        icon = auto()
        lock = auto()
        breakpoint = auto()
        hidden = auto()
        color = auto()
        pins = auto()
        tags = auto()
        head_height = auto()
        exec_height = auto()
        data_height = auto()
        icon_pos = auto()
        icon_size = auto()
        name_pos = auto()
        name_size = auto()
        node_pos = auto()
        node_size = auto()

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        uuid: Optional[NodeKey] = None,
        name: Optional[NodeName] = None,
        path: Optional[NodePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        lock=False,
        breakpoint=False,
        hidden=False,
        color: RGBA = WHITE_RGBA,
        pins: Optional[Union[FlowPins, Iterable[FlowPin]]] = None,
        tags: Optional[Iterable[str]] = None,
        head_height=0.0,
        exec_height=0.0,
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
        self.uuid = uuid if uuid else NodeKey(str(uuid4()))
        self.name = name if name else NodeName(str())
        self.path = path if path else NodePath(str())
        self.docs = docs if docs else str()
        self.icon = icon if icon else IconCode(str())

        self.lock = lock
        self.breakpoint = breakpoint
        self.hidden = hidden
        self.color = color

        if pins is None:
            self.pins = FlowPins()
        elif isinstance(pins, FlowPins):
            self.pins = pins
        elif isinstance(pins, Iterable):
            self.pins = FlowPins(list(pins if pins else ()))
        else:
            raise TypeError(f"Unsupported pins type: {type(pins).__name__}")

        self.tags = list(tags if tags else ())

        self.head_height = head_height
        self.exec_height = exec_height
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
    def from_template(cls, template: NodeTemplate):
        return cls(
            uuid=NodeKey(str(uuid4())),
            name=template.name,
            path=template.path,
            docs=template.docs,
            icon=template.icon,
            lock=False,
            breakpoint=False,
            hidden=False,
            color=template.color,
            pins=FlowPins.from_template(template.pins),
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
            and self.pins == other.pins
            and self.tags == other.tags
            and self.head_height == other.head_height
            and self.exec_height == other.exec_height
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
        result.pins = copy(self.pins)
        result.tags = copy(self.tags)
        result.head_height = copy(self.head_height)
        result.exec_height = copy(self.exec_height)
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
        result.pins = deepcopy(self.pins, memo)
        result.tags = deepcopy(self.tags, memo)
        result.head_height = deepcopy(self.head_height, memo)
        result.exec_height = deepcopy(self.exec_height, memo)
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
        return {
            str(self._Keys.uuid): str(self.uuid),
            str(self._Keys.name_): str(self.name),
            str(self._Keys.path): str(self.path),
            str(self._Keys.docs): str(self.docs),
            str(self._Keys.icon): str(self.icon),
            str(self._Keys.lock): bool(self.lock),
            str(self._Keys.breakpoint): bool(self.breakpoint),
            str(self._Keys.hidden): bool(self.hidden),
            str(self._Keys.color): list(self.color),
            str(self._Keys.pins): serialize(self.pins),
            str(self._Keys.tags): list(self.tags),
            str(self._Keys.head_height): float(self.head_height),
            str(self._Keys.exec_height): float(self.exec_height),
            str(self._Keys.data_height): float(self.data_height),
            str(self._Keys.icon_pos): list(self.icon_pos),
            str(self._Keys.icon_size): list(self.icon_size),
            str(self._Keys.name_pos): list(self.name_pos),
            str(self._Keys.name_size): list(self.name_size),
            str(self._Keys.node_pos): list(self.node_pos),
            str(self._Keys.node_size): list(self.node_size),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = NodeKey(data.get(self._Keys.uuid, str()))
        self.name = NodeName(data.get(self._Keys.name_, str()))
        self.path = NodePath(data.get(self._Keys.path, str()))
        self.docs = data.get(self._Keys.docs, str())
        self.icon = IconCode(data.get(self._Keys.icon, str()))
        self.lock = data.get(self._Keys.lock, False)
        self.breakpoint = data.get(self._Keys.breakpoint, False)
        self.hidden = data.get(self._Keys.hidden, False)

        self.color = tuple(data.get(self._Keys.color, WHITE_RGBA))
        assert len(self.color) == 4

        pins = data.get(self._Keys.pins)
        if pins is None:
            self.pins = FlowPins()
        elif isinstance(pins, list):
            self.pins = deserialize(pins, FlowPins)
        else:
            raise TypeError(f"Unsupported pins type: {type(pins).__name__}")

        self.tags = data.get(self._Keys.tags, list())

        self.head_height = data.get(self._Keys.head_height, 0.0)
        self.exec_height = data.get(self._Keys.exec_height, 0.0)
        self.data_height = data.get(self._Keys.data_height, 0.0)

        self.icon_pos = tuple(data.get(self._Keys.icon_pos, EMPTY_POINT))
        self.icon_size = tuple(data.get(self._Keys.icon_size, EMPTY_SIZE))
        self.name_pos = tuple(data.get(self._Keys.name_pos, EMPTY_POINT))
        self.name_size = tuple(data.get(self._Keys.name_size, EMPTY_SIZE))
        self.node_pos = tuple(data.get(self._Keys.node_pos, EMPTY_POINT))
        self.node_size = tuple(data.get(self._Keys.node_size, EMPTY_SIZE))

        assert len(self.icon_pos) == 2
        assert len(self.icon_size) == 2
        assert len(self.name_pos) == 2
        assert len(self.name_size) == 2
        assert len(self.node_pos) == 2
        assert len(self.node_size) == 2

        self._selected = False
        self._hovering = False

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
    def exec_outputs(self):
        return self.pins.as_exec_outputs()

    @property
    def exec_inputs(self):
        return self.pins.as_exec_inputs()

    @property
    def data_outputs(self):
        return self.pins.as_data_outputs()

    @property
    def data_inputs(self):
        return self.pins.as_data_inputs()

    @property
    def exec_pins(self) -> List[FlowPin]:
        return self.pins.as_execs()

    @property
    def data_pins(self) -> List[FlowPin]:
        return self.pins.as_datas()

    @property
    def input_pins(self) -> List[FlowPin]:
        return self.pins.as_inputs()

    @property
    def output_pins(self) -> List[FlowPin]:
        return self.pins.as_outputs()

    @property
    def is_data_only(self) -> bool:
        return self.pins.is_data_only()

    @property
    def is_begin(self) -> bool:
        return self.pins.is_begin()

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
            f"Pins: {len(self.pins)}\n"
            f"Tags: {self.tags}\n"
            f"Head height: {self.head_height:.02f}\n"
            f"Flow height: {self.exec_height:.02f}\n"
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

    def find_output_pin(self, wire_uuid: str) -> Optional[FlowPin]:
        for pin in self.output_pins:
            if wire_uuid in pin.wires:
                return pin
        return None

    def find_input_pin(self, wire_uuid: str) -> Optional[FlowPin]:
        for pin in self.input_pins:
            if wire_uuid in pin.wires:
                return pin
        return None

    def remove_wire_from_pins(self, wire_uuid: str) -> None:
        for pin in self.pins:
            try:
                pin.wires.remove(wire_uuid)
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

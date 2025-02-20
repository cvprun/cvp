# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Optional, Sequence

from type_serialize import Serializable

from cvp.pins.action import Action
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream
from cvp.types.override import override
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size


@unique
class FlowPinKeys(StrEnum):
    name_ = "name"
    docs = auto()
    dtype = auto()
    action = auto()
    stream = auto()
    required = auto()
    hidden = auto()
    arcs = auto()
    icon_pos = auto()
    icon_size = auto()
    name_pos = auto()
    name_size = auto()


class FlowPin(Serializable):
    Keys = FlowPinKeys

    def __init__(
        self,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        dtype: Optional[str] = None,
        action=Action.data,
        stream=Stream.input,
        required=False,
        hidden=False,
        arcs: Optional[Sequence[str]] = None,
        icon_pos: Point = EMPTY_POINT,
        icon_size: Size = EMPTY_SIZE,
        name_pos: Point = EMPTY_POINT,
        name_size: Size = EMPTY_SIZE,
        *,
        template: Optional[Pin] = None,
        selected=False,
        hovering=False,
        connectable=False,
    ):
        self.name = name if name else str()
        self.docs = docs if docs else str()
        self.dtype = dtype if dtype else str()
        self.action = action
        self.stream = stream
        self.required = required
        self.hidden = hidden
        self.arcs = list(arcs if arcs else list())

        self.icon_pos = icon_pos
        self.icon_size = icon_size

        self.name_pos = name_pos
        self.name_size = name_size

        self._template = template
        self._selected = selected
        self._hovering = hovering
        self._connectable = connectable

    @classmethod
    def from_template(cls, template: Pin):
        return cls(
            name=template.name,
            docs=template.docs,
            dtype=template.path,
            action=template.action,
            stream=template.stream,
            required=template.required,
            hidden=template.hidden,
            arcs=deepcopy(template.arcs),
            template=template,
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.docs = copy(self.docs)
        result.dtype = copy(self.dtype)
        result.action = copy(self.action)
        result.stream = copy(self.stream)
        result.required = copy(self.required)
        result.hidden = copy(self.hidden)
        result.arcs = copy(self.arcs)
        result.icon_pos = copy(self.icon_pos)
        result.icon_size = copy(self.icon_size)
        result.name_pos = copy(self.name_pos)
        result.name_size = copy(self.name_size)
        result._template = copy(self._template)
        result._selected = copy(self._selected)
        result._hovering = copy(self._hovering)
        result._connectable = copy(self._connectable)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = deepcopy(self.name, memo)
        result.docs = deepcopy(self.docs, memo)
        result.dtype = deepcopy(self.dtype, memo)
        result.action = deepcopy(self.action, memo)
        result.stream = deepcopy(self.stream, memo)
        result.required = deepcopy(self.required, memo)
        result.hidden = deepcopy(self.hidden, memo)
        result.arcs = deepcopy(self.arcs, memo)
        result.icon_pos = deepcopy(self.icon_pos, memo)
        result.icon_size = deepcopy(self.icon_size, memo)
        result.name_pos = deepcopy(self.name_pos, memo)
        result.name_size = deepcopy(self.name_size, memo)
        result._template = deepcopy(self._template, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        result._connectable = deepcopy(self._connectable, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self.Keys.name_: self.name,
            self.Keys.docs: self.docs,
            self.Keys.dtype: self.dtype,
            self.Keys.action: str(self.action),
            self.Keys.stream: str(self.stream),
            self.Keys.required: self.required,
            self.Keys.hidden: self.hidden,
            self.Keys.arcs: self.arcs,
            self.Keys.icon_pos: self.icon_pos,
            self.Keys.icon_size: self.icon_size,
            self.Keys.name_pos: self.name_pos,
            self.Keys.name_size: self.name_size,
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.name = data.get(self.Keys.name_, str())
        self.docs = data.get(self.Keys.docs, str())
        self.dtype = data.get(self.Keys.dtype, str())

        if action := data.get(self.Keys.action):
            self.action = Action(action)
        else:
            self.action = Action.data

        if stream := data.get(self.Keys.stream):
            self.stream = Stream(stream)
        else:
            self.stream = Stream.input

        self.required = data.get(self.Keys.required, False)
        self.hidden = data.get(self.Keys.hidden, False)
        self.arcs = data.get(self.Keys.arcs, list())
        self.icon_pos = data.get(self.Keys.icon_pos, EMPTY_POINT)
        self.icon_size = data.get(self.Keys.icon_size, EMPTY_SIZE)
        self.name_pos = data.get(self.Keys.name_pos, EMPTY_POINT)
        self.name_size = data.get(self.Keys.name_size, EMPTY_SIZE)

        self._template = None
        self._selected = False
        self._hovering = False
        self._connectable = False

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value: Pin) -> None:
        self._template = value

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
            f"Hidden: {self.hidden}\n"
            f"Arcs: {len(self.arcs)}\n"
            f"Icon pos: {self.icon_pos[0]:.02f}, {self.icon_pos[1]:.02f}\n"
            f"Icon size: {self.icon_size[0]:.02f}, {self.icon_size[1]:.02f}\n"
            f"Name pos: {self.name_pos[0]:.02f}, {self.name_pos[1]:.02f}\n"
            f"Name size: {self.name_size[0]:.02f}, {self.name_size[1]:.02f}\n"
            f"Selected: {self._selected}\n"
            f"Hovering: {self._hovering}\n"
            f"Connectable: {self._connectable}\n"
        )

# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Literal, Optional, Sequence, Union

from type_serialize import Serializable, deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.raw_value import dumps, loads
from cvp.pins.action import Action, create_action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream, create_stream
from cvp.pins.template import PinTemplate
from cvp.types.override import override
from cvp.types.shapes import EMPTY_POINT, EMPTY_SIZE, Point, Rect, Size


class FlowPin(Serializable):

    @unique
    class _Keys(StrEnum):
        name_ = "name"
        docs = auto()
        dtype = auto()
        action = auto()
        stream = auto()
        required = auto()
        hidden = auto()
        wires = auto()
        kind = auto()
        default = auto()
        icon_pos = auto()
        icon_size = auto()
        name_pos = auto()
        name_size = auto()

    def __init__(
        self,
        name: str,
        dtype: Dtype,
        action: Union[Action, Literal["exec", "data", 0, 1]],
        stream: Union[Stream, Literal["input", "output", 0, 1]],
        docs: Optional[str] = None,
        required=False,
        hidden=False,
        wires: Optional[Sequence[str]] = None,
        kind: Optional[PinKind] = None,
        default: Any = None,
        icon_pos: Point = EMPTY_POINT,
        icon_size: Size = EMPTY_SIZE,
        name_pos: Point = EMPTY_POINT,
        name_size: Size = EMPTY_SIZE,
        *,
        selected=False,
        hovering=False,
        connectable=False,
    ):
        self.name = name
        self.dtype = dtype
        self.action = create_action(action)
        self.stream = create_stream(stream)

        self.docs = docs if docs else str()
        self.required = required
        self.hidden = hidden
        self.wires = list(wires if wires else ())
        self.kind = kind if kind is not None else PinKind.unknown
        self.default = default

        self.icon_pos = icon_pos
        self.icon_size = icon_size

        self.name_pos = name_pos
        self.name_size = name_size

        self._selected = selected
        self._hovering = hovering
        self._connectable = connectable

    @classmethod
    def from_template(cls, template: PinTemplate):
        return cls(
            name=template.name,
            dtype=template.dtype,
            action=template.action,
            stream=template.stream,
            docs=template.docs,
            required=template.required,
            hidden=template.hidden,
            wires=deepcopy(template.wires),
            kind=template.kind,
            default=deepcopy(template.default) if template.has_default else None,
        )

    def __str__(self) -> str:
        """In `cvp.flow` module, this return value is used as a key value."""
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.name == other.name
            and self.dtype == other.dtype
            and self.action == other.action
            and self.stream == other.stream
            and self.docs == other.docs
            and self.required == other.required
            and self.hidden == other.hidden
            and self.wires == other.wires
            and self.kind == other.kind
            and self.default == other.default
            and self.icon_pos == other.icon_pos
            and self.icon_size == other.icon_size
            and self.name_pos == other.name_pos
            and self.name_size == other.name_size
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.dtype = copy(self.dtype)
        result.action = copy(self.action)
        result.stream = copy(self.stream)
        result.docs = copy(self.docs)
        result.required = copy(self.required)
        result.hidden = copy(self.hidden)
        result.wires = copy(self.wires)
        result.kind = copy(self.kind)
        result.default = copy(self.default)
        result.icon_pos = copy(self.icon_pos)
        result.icon_size = copy(self.icon_size)
        result.name_pos = copy(self.name_pos)
        result.name_size = copy(self.name_size)
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
        result.dtype = deepcopy(self.dtype, memo)
        result.action = deepcopy(self.action, memo)
        result.stream = deepcopy(self.stream, memo)
        result.docs = deepcopy(self.docs, memo)
        result.required = deepcopy(self.required, memo)
        result.hidden = deepcopy(self.hidden, memo)
        result.wires = deepcopy(self.wires, memo)
        result.kind = deepcopy(self.kind, memo)
        result.default = deepcopy(self.default, memo)
        result.icon_pos = deepcopy(self.icon_pos, memo)
        result.icon_size = deepcopy(self.icon_size, memo)
        result.name_pos = deepcopy(self.name_pos, memo)
        result.name_size = deepcopy(self.name_size, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        result._connectable = deepcopy(self._connectable, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self._Keys.name_: self.name,
            self._Keys.dtype: serialize(self.dtype),
            self._Keys.action: str(self.action),
            self._Keys.stream: str(self.stream),
            self._Keys.docs: self.docs,
            self._Keys.required: self.required,
            self._Keys.hidden: self.hidden,
            self._Keys.wires: self.wires,
            self._Keys.kind: int(self.kind),
            self._Keys.default: dumps(self.default),
            self._Keys.icon_pos: list(self.icon_pos),
            self._Keys.icon_size: list(self.icon_size),
            self._Keys.name_pos: list(self.name_pos),
            self._Keys.name_size: list(self.name_size),
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        name = data.get(self._Keys.name_)
        if not name:
            raise ValueError(f"The '{self._Keys.name_}' attribute is required")
        if not isinstance(name, str):
            raise TypeError(f"The '{self._Keys.name_}' attribute only allows str type")

        dtype = data.get(self._Keys.dtype)
        if dtype is None:
            raise ValueError(f"The '{self._Keys.dtype}' attribute is required")

        action = data.get(self._Keys.action)
        if action is None:
            raise ValueError(f"The '{self._Keys.action}' attribute is required")

        stream = data.get(self._Keys.stream)
        if stream is None:
            raise ValueError(f"The '{self._Keys.stream}' attribute is required")

        self.name = name
        self.dtype = deserialize(dtype, Dtype)
        self.action = create_action(action)
        self.stream = create_stream(stream)
        self.docs = data.get(self._Keys.docs, str())
        self.required = data.get(self._Keys.required, False)
        self.hidden = data.get(self._Keys.hidden, False)
        self.wires = data.get(self._Keys.wires, list())

        kind = data.get(self._Keys.kind)
        if kind is not None:
            assert isinstance(kind, int)
            self.kind = PinKind(kind)
        else:
            self.kind = PinKind.unknown

        self.default = loads(data.get(self._Keys.default, None))

        self.icon_pos = tuple(data.get(self._Keys.icon_pos, EMPTY_POINT))
        self.icon_size = tuple(data.get(self._Keys.icon_size, EMPTY_SIZE))
        self.name_pos = tuple(data.get(self._Keys.name_pos, EMPTY_POINT))
        self.name_size = tuple(data.get(self._Keys.name_size, EMPTY_SIZE))

        assert len(self.icon_pos) == 2
        assert len(self.icon_size) == 2
        assert len(self.name_pos) == 2
        assert len(self.name_size) == 2

        self._selected = False
        self._hovering = False
        self._connectable = False

    @property
    def is_data_action(self):
        return self.action == Action.data

    @property
    def is_exec_action(self):
        return self.action == Action.exec

    @property
    def is_input_stream(self):
        return self.stream == Stream.input

    @property
    def is_output_stream(self):
        return self.stream == Stream.output

    @property
    def is_exec_inputs(self) -> bool:
        return self.is_exec_action and self.is_input_stream

    @property
    def is_exec_outputs(self) -> bool:
        return self.is_exec_action and self.is_output_stream

    @property
    def is_data_inputs(self) -> bool:
        return self.is_data_action and self.is_input_stream

    @property
    def is_data_outputs(self) -> bool:
        return self.is_data_action and self.is_output_stream

    @property
    def connected(self) -> bool:
        return bool(self.wires)

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
            f"Arcs: {len(self.wires)}\n"
            f"Kind: {self.kind}\n"
            f"Default: {self.default}\n"
            f"Icon pos: {self.icon_pos[0]:.02f}, {self.icon_pos[1]:.02f}\n"
            f"Icon size: {self.icon_size[0]:.02f}, {self.icon_size[1]:.02f}\n"
            f"Name pos: {self.name_pos[0]:.02f}, {self.name_pos[1]:.02f}\n"
            f"Name size: {self.name_size[0]:.02f}, {self.name_size[1]:.02f}\n"
            f"Selected: {self._selected}\n"
            f"Hovering: {self._hovering}\n"
            f"Connectable: {self._connectable}\n"
        )

    def get_initial_value(self) -> Any:
        if self.default is not None:
            return deepcopy(self.default)  # It should not affect the original value
        else:
            if self.dtype.type == Any:
                return object()
            else:
                return self.dtype.type()

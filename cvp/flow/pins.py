# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Callable, Dict, Final, Iterable, List, Optional, SupportsIndex, Union

from type_serialize import Serializable, deserialize, serialize

from cvp.containers.mapping_deque import MappingDeque
from cvp.flow.pin import FlowPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import PREV_PIN_NAME, NEXT_PIN_NAME, RETURN_PIN_NAME, EmptyNextPin
from cvp.types.override import override

_EMPTY_NEXT_FLOW_PIN: Final[FlowPin] = FlowPin.from_template(EmptyNextPin())


class FlowPins(Serializable):
    def __init__(self, pins: Optional[Iterable[FlowPin]] = None):
        self.pins = self.__create_map(list(pins if pins else ()))

    @staticmethod
    def __pin_keyable(pin: FlowPin) -> PinName:
        return pin.name

    @staticmethod
    def __create_map(pins: List[FlowPin]):
        return MappingDeque[PinName, FlowPin](pins, keyable=FlowPins.__pin_keyable)

    @staticmethod
    def nonext():
        return copy(_EMPTY_NEXT_FLOW_PIN)

    @classmethod
    def from_template(cls, templates: Optional[Iterable[Pin]] = None):
        pins = list()
        if templates:
            for template in templates:
                pins.append(FlowPin.from_template(template))
        return cls(pins)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.pins == other.pins

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.pins = copy(self.pins)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.pins = deepcopy(self.pins, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return list(serialize(pin) for pin in self.pins)

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, list):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")
        self.pins = self.__create_map(list(deserialize(d, FlowPin) for d in data))

    def as_list(self):
        return self.pins.as_list()

    def as_dict(self):
        return self.pins.as_dict()

    def __len__(self) -> int:
        return self.pins.__len__()

    def __contains__(self, key: PinName) -> bool:
        return self.pins.__contains__(key)

    def __getitem__(self, key: Union[SupportsIndex, PinName]) -> FlowPin:
        return self.pins.__getitem__(key)

    def __setitem__(self, key: Union[SupportsIndex, PinName], value: FlowPin) -> None:
        self.pins.__setitem__(key, value)

    def __delitem__(self, key: Union[SupportsIndex, PinName]) -> None:
        self.pins.__delitem__(key)

    def __iter__(self):
        return self.pins.__iter__()

    def __reversed__(self):
        return self.pins.__reversed__()

    def __iadd__(self, other: Iterable[FlowPin]):
        return self.pins.__iadd__(other)

    def items(self):
        return self.pins.items()

    def keys(self):
        return self.pins.keys()

    def values(self):
        return self.pins.values()

    def index(self, value: FlowPin, start=0, stop: Optional[int] = None) -> int:
        return self.pins.index(value, start, stop)

    def clear(self) -> None:
        self.pins.clear()

    def filter(self, func: Callable[[FlowPin], bool], *, visible_only=False):
        if visible_only:
            return type(self)(filter(lambda p: func(p) and not p.hidden, self.pins))
        else:
            return type(self)(filter(lambda p: func(p), self.pins))

    def as_exec_inputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_exec_inputs, visible_only=visible_only)

    def as_exec_outputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_exec_outputs, visible_only=visible_only)

    def as_data_inputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_data_inputs, visible_only=visible_only)

    def as_data_outputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_data_outputs, visible_only=visible_only)

    def as_execs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_exec_action, visible_only=visible_only)

    def as_datas(self, *, visible_only=False):
        return self.filter(lambda p: p.is_data_action, visible_only=visible_only)

    def as_inputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_input_stream, visible_only=visible_only)

    def as_outputs(self, *, visible_only=False):
        return self.filter(lambda p: p.is_output_stream, visible_only=visible_only)

    # fmt: off

    def get_exec_lines(self, *, visible_only=False) -> int:
        return max(
            len(self.as_exec_inputs(visible_only=visible_only)),
            len(self.as_exec_outputs(visible_only=visible_only)),
        )

    def get_data_lines(self, *, visible_only=False) -> int:
        return max(
            len(self.as_data_inputs(visible_only=visible_only)),
            len(self.as_data_outputs(visible_only=visible_only)),
        )

    def has_exec_input(self, *, visible_only=False) -> bool:
        return bool(self.as_exec_inputs(visible_only=visible_only))

    def has_exec_output(self, *, visible_only=False) -> bool:
        return bool(self.as_exec_outputs(visible_only=visible_only))

    def has_data_input(self, *, visible_only=False) -> bool:
        return bool(self.as_data_inputs(visible_only=visible_only))

    def has_data_output(self, *, visible_only=False) -> bool:
        return bool(self.as_data_outputs(visible_only=visible_only))

    def is_any_exec(self, *, visible_only=False) -> bool:
        return (
            self.has_exec_input(visible_only=visible_only)
            or self.has_exec_output(visible_only=visible_only)
        )

    def is_any_data(self, *, visible_only=False) -> bool:
        return (
            self.has_data_input(visible_only=visible_only)
            or self.has_data_output(visible_only=visible_only)
        )

    def is_any_input(self, *, visible_only=False) -> bool:
        return (
            self.has_exec_input(visible_only=visible_only)
            or self.has_data_input(visible_only=visible_only)
        )

    def is_any_output(self, *, visible_only=False) -> bool:
        return (
            self.has_exec_output(visible_only=visible_only)
            or self.has_data_output(visible_only=visible_only)
        )

    def is_exec_only(self, *, visible_only=False) -> bool:
        return (
            self.is_any_exec(visible_only=visible_only)
            and not self.is_any_data(visible_only=visible_only)
        )

    def is_data_only(self, *, visible_only=False) -> bool:
        return (
            not self.is_any_exec(visible_only=visible_only)
            and self.is_any_data(visible_only=visible_only)
        )

    def is_input_only(self, *, visible_only=False) -> bool:
        return (
            self.is_any_input(visible_only=visible_only)
            and not self.is_any_output(visible_only=visible_only)
        )

    def is_output_only(self, *, visible_only=False) -> bool:
        return (
            not self.is_any_input(visible_only=visible_only)
            and self.is_any_output(visible_only=visible_only)
        )

    def is_begin(self, *, visible_only=False) -> bool:
        return (
            not self.has_exec_input(visible_only=visible_only)
            and self.has_exec_output(visible_only=visible_only)
        )

    def is_middle(self, *, visible_only=False) -> bool:
        return (
            self.has_exec_input(visible_only=visible_only)
            and self.has_exec_output(visible_only=visible_only)
        )

    def is_end(self, *, visible_only=False) -> bool:
        return (
            self.has_exec_input(visible_only=visible_only)
            and not self.has_exec_output(visible_only=visible_only)
        )

    # fmt: on

    def is_bypass_exec(self) -> bool:
        if len(self.as_execs()) != 2:
            return False

        exec_inputs = self.as_exec_inputs()
        if len(exec_inputs) != 1:
            return False

        exec_outputs = self.as_exec_outputs()
        if len(exec_outputs) != 1:
            return False

        if exec_inputs[0].name != PREV_PIN_NAME:
            return False
        if exec_outputs[0].name != NEXT_PIN_NAME:
            return False

        return True

    def find_return_pin(self) -> Optional[FlowPin]:
        for pin in self.pins:
            if pin.name == RETURN_PIN_NAME:
                return pin
        return None

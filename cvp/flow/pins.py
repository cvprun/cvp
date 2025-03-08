# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Dict, Iterable, List, Optional, Sequence, SupportsIndex, Union

from type_serialize import Serializable, deserialize, serialize

from cvp.containers.mapping_deque import MappingDeque
from cvp.flow.pin import FlowPin
from cvp.pins.template import PinTemplate
from cvp.types.override import override


class FlowPins(Serializable):
    def __init__(self, pins: Optional[Sequence[FlowPin]] = None):
        self.pins = self.__create_map(list(pins if pins else ()))

    @staticmethod
    def __pin_keyable(pin: FlowPin) -> str:
        return pin.name

    @staticmethod
    def __create_map(pins: List[FlowPin]):
        return MappingDeque[str, FlowPin](pins, keyable=FlowPins.__pin_keyable)

    @classmethod
    def from_template(cls, templates: Optional[Sequence[PinTemplate]] = None):
        pins = list()
        if templates:
            for template in templates:
                pins.append(FlowPin.from_template(template))
        return cls(pins)

    def as_list(self):
        return self.pins.as_list()

    def as_dict(self):
        return self.pins.as_dict()

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.pins == other.pins

    def __len__(self) -> int:
        return self.pins.__len__()

    def __contains__(self, key: str) -> bool:
        return self.pins.__contains__(key)

    def __getitem__(self, key: Union[SupportsIndex, str]) -> FlowPin:
        return self.pins.__getitem__(key)

    def __setitem__(self, key: Union[SupportsIndex, str], value: FlowPin) -> None:
        self.pins.__setitem__(key, value)

    def __delitem__(self, key: Union[SupportsIndex, str]) -> None:
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

    def clear(self) -> None:
        self.pins.clear()

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

    @property
    def exec_inputs(self):
        return list(filter(lambda p: p.is_exec_inputs(), self.pins))

    @property
    def exec_outputs(self):
        return list(filter(lambda p: p.is_exec_outputs(), self.pins))

    @property
    def data_inputs(self):
        return list(filter(lambda p: p.is_data_inputs(), self.pins))

    @property
    def data_outputs(self):
        return list(filter(lambda p: p.is_data_outputs(), self.pins))

    @property
    def inputs(self):
        return list(filter(lambda p: p.is_input_stream(), self.pins))

    @property
    def outputs(self):
        return list(filter(lambda p: p.is_output_stream(), self.pins))

    @property
    def execs(self):
        return list(filter(lambda p: p.is_exec_action(), self.pins))

    @property
    def datas(self):
        return list(filter(lambda p: p.is_data_action(), self.pins))

    @property
    def exec_lines(self):
        return max(len(self.exec_inputs), len(self.exec_outputs))

    @property
    def data_lines(self):
        return max(len(self.data_inputs), len(self.data_outputs))

    @property
    def has_exec_input(self) -> bool:
        return bool(self.exec_inputs)

    @property
    def has_exec_output(self) -> bool:
        return bool(self.exec_outputs)

    @property
    def has_data_input(self) -> bool:
        return bool(self.data_inputs)

    @property
    def has_data_output(self) -> bool:
        return bool(self.data_outputs)

    @property
    def any_exec(self) -> bool:
        return self.has_exec_input or self.has_exec_output

    @property
    def any_data(self) -> bool:
        return self.has_data_input or self.has_data_output

    @property
    def is_exec_only(self) -> bool:
        return self.any_exec and not self.any_data

    @property
    def is_data_only(self) -> bool:
        return not self.any_exec and self.any_data

    @property
    def is_begin(self) -> bool:
        return not self.has_exec_input and self.has_exec_output

    @property
    def is_middle(self) -> bool:
        return self.has_exec_input and self.has_exec_output

    @property
    def is_end(self) -> bool:
        return self.has_exec_input and not self.has_exec_output

# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Dict, Iterable, List, Optional, SupportsIndex, Union

from type_serialize import Serializable, deserialize, serialize

from cvp.containers.mapping_deque import MappingDeque
from cvp.flow.pin import FlowPin
from cvp.pins.template import PinTemplate
from cvp.types.override import override


class FlowPins(Serializable):
    def __init__(self, pins: Optional[Iterable[FlowPin]] = None):
        self.pins = self.__create_map(list(pins if pins else ()))

    @staticmethod
    def __pin_keyable(pin: FlowPin) -> str:
        return pin.name

    @staticmethod
    def __create_map(pins: List[FlowPin]):
        return MappingDeque[str, FlowPin](pins, keyable=FlowPins.__pin_keyable)

    @classmethod
    def from_template(cls, templates: Optional[Iterable[PinTemplate]] = None):
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

    def as_exec_inputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_exec_inputs and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_exec_inputs, self.pins))

    def as_exec_outputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_exec_outputs and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_exec_outputs, self.pins))

    def as_data_inputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_data_inputs and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_data_inputs, self.pins))

    def as_data_outputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_data_outputs and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_data_outputs, self.pins))

    def as_execs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_exec_action and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_exec_action, self.pins))

    def as_datas(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_data_action and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_data_action, self.pins))

    def as_inputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_input_stream and not p.hidden, self.pins))
        else:
            return list(filter(lambda p: p.is_input_stream, self.pins))

    # fmt: off

    def as_outputs(self, *, visible_only=False) -> List[FlowPin]:
        if visible_only:
            return list(filter(lambda p: p.is_output_stream and not p.hidden, self.pins))  # noqa: E501
        else:
            return list(filter(lambda p: p.is_output_stream, self.pins))

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

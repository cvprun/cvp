# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Dict, Optional, Sequence, TypeAlias

from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream
from cvp.variables import FLOW_PATH_SEPARATOR

VariableKey: TypeAlias = str
VariableVal: TypeAlias = Any


class NodeVariableStore(Dict[VariableKey, VariableVal]):
    @classmethod
    def from_other(
        cls,
        other: Optional["NodeVariableStore"] = None,
        *,
        use_copy=False,
        use_deepcopy=False,
    ):
        if use_copy and use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist.")

        if other is not None:
            if use_copy:
                return other.copy()
            elif use_deepcopy:
                return deepcopy(other)
            else:
                return other
        else:
            return cls()

    @staticmethod
    def gen_pin_key(node_uuid: str, pin_name: str) -> VariableKey:
        return node_uuid + FLOW_PATH_SEPARATOR + pin_name

    def get_pin_value(self, node_uuid: str, pin: Pin) -> Any:
        key = self.gen_pin_key(node_uuid, pin.name)
        if self.__contains__(key):
            return self.__getitem__(key)

        if pin.dtype is not None:
            if pin.has_default:
                value = pin.dtype.base(pin.default)
            else:
                value = pin.dtype.base()
        else:
            if pin.has_default:
                value = deepcopy(pin.default)  # It should not affect the original value
            else:
                value = None

        self.__setitem__(key, value)
        return value

    def create_node_execution_record(
        self,
        node_uuid: str,
        data_pins: Sequence[Pin],
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> NodeExecutionRecord:
        if use_copy and use_deepcopy:
            raise ValueError("'use_copy' and 'use_deepcopy' cannot coexist")

        variables = dict()
        bind_args = list()
        bind_kwargs = dict()
        result_key = str()

        for pin in data_pins:
            if not pin.is_data_action:
                raise ValueError(f"Only '{Action.data}' are allowed")

            value = self.get_pin_value(node_uuid, pin)
            if use_copy:
                value = copy(value)
            elif use_deepcopy:
                value = deepcopy(value)

            match pin.stream:
                case Stream.input:
                    variables[pin.name] = value
                case Stream.output:
                    variables[pin.name] = value
                case _:
                    assert False, "Inaccessible section"

            if pin.kind is not None:
                match pin.kind:
                    case PinKind.unknown:
                        pass
                    case PinKind.positional_only:
                        bind_args.append(value)
                    case PinKind.positional_or_keyword:
                        bind_kwargs[pin.name] = value
                    case PinKind.var_positional:
                        bind_args.append(value)
                    case PinKind.keyword_only:
                        bind_kwargs[pin.name] = value
                    case PinKind.var_keyword:
                        bind_kwargs[pin.name] = value
                    case PinKind.return_only:
                        result_key = pin.name
                    case PinKind.flow_only:
                        assert False, "Inaccessible section"
                    case _:
                        assert False, "Inaccessible section"

        return NodeExecutionRecord(variables, bind_args, bind_kwargs, result_key)

    def update_with_node_execution_record(
        self,
        node_uuid: str,
        record: NodeExecutionRecord,
    ) -> None:
        for pin_name, pin_variable in record.variables.items():
            key = self.gen_pin_key(node_uuid, pin_name)
            self.__setitem__(key, pin_variable)

        if not record.has_exception:
            if record.result_key:
                key = self.gen_pin_key(node_uuid, record.result_key)
                self.__setitem__(key, record.result)

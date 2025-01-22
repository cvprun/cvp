# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Dict, Optional, TypeAlias

from cvp.nodes.node import Node
from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream
from cvp.variables import FLOW_PATH_SEPARATOR

VariableKey: TypeAlias = str
VariableVal: TypeAlias = Any


class VariableStore(Dict[VariableKey, VariableVal]):
    @classmethod
    def from_other(
        cls,
        other: Optional["VariableStore"] = None,
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
    def gen_pin_key(node_uuid: str, pin_name: str):
        return node_uuid + FLOW_PATH_SEPARATOR + pin_name

    def get_pin_value(self, node_uuid: str, pin: Pin) -> Any:
        key = self.gen_pin_key(node_uuid, pin.name)
        if pin.has_default:
            return self.get(key, pin.has_default)

        if not self.__contains__(key):
            raise KeyError(f"Not found variable: '{key}'")

        return self.__getitem__(key)

    def create_node_execution_record(
        self,
        node: Node,
        node_uuid: str,
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> NodeExecutionRecord:
        if use_copy and use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist.")

        inputs = dict()
        outputs = dict()

        bind_args = list()
        bind_kwargs = dict()

        for pin in node.datas:
            value = self.get_pin_value(node_uuid, pin)
            if use_copy:
                value = copy(value)
            elif use_deepcopy:
                value = deepcopy(value)

            match pin.stream:
                case Stream.input:
                    inputs[pin.name] = value
                case Stream.output:
                    outputs[pin.name] = value
                case _:
                    assert False, "Inaccessible section"

            if pin.kind is not None:
                match pin.kind:
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
                    case _:
                        assert False, "Inaccessible section"

        return NodeExecutionRecord(
            inputs=inputs,
            outputs=outputs,
            args=bind_args,
            kwargs=bind_kwargs,
        )

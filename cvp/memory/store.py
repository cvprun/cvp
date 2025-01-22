# -*- coding: utf-8 -*-

from typing import Any, Dict, TypeAlias

from cvp.nodes.node import Node
from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.variables import FLOW_PATH_SEPARATOR

VariableKey: TypeAlias = str
VariableVal: TypeAlias = Any
VariableRaw: TypeAlias = Dict[VariableKey, VariableVal]


class VariableStore(VariableRaw):
    def create_node_execution_record(
        self,
        node: Node,
        node_uuid: str,
    ) -> NodeExecutionRecord:
        inputs = dict()
        outputs = dict()

        bind_args = list()
        bind_kwargs = dict()

        for pin in node.datas:
            key = node_uuid + FLOW_PATH_SEPARATOR + pin.name
            value = self.get(key, pin.default)

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

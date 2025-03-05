# -*- coding: utf-8 -*-

from collections import deque
from copy import copy, deepcopy
from typing import Any, Deque, Dict, Mapping, NamedTuple, NewType, Optional, Sequence

from cvp.flow.graph import FlowGraph
from cvp.flow.pin import FlowPin
from cvp.flow.variable import FlowVariable
from cvp.nodes.record import NodeRecord
from cvp.patterns.proxy import ValueProxy
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.variables import FLOW_PATH_SEPARATOR

WireKey = NewType("WireKey", str)


class PinKey(NamedTuple):
    node_uuid: str
    pin_name: str

    def __str__(self):
        return self.node_uuid + FLOW_PATH_SEPARATOR + self.pin_name


class FlowMemory:
    _datas: Deque[Any]
    _pins: Dict[PinKey, int]
    _wires: Dict[WireKey, int]
    _vars: Dict[str, ValueProxy]

    def __init__(self):
        self._datas = deque()
        self._pins = dict()
        self._wires = dict()
        self._vars = dict()

    def clear(self):
        self._datas.clear()
        self._pins.clear()
        self._wires.clear()
        self._vars.clear()

    def __insert_output_datas(self, node_uuid: str, pins: Sequence[FlowPin]) -> None:
        for pin in pins:
            assert pin.is_data_outputs
            pin_key = PinKey(node_uuid, pin.name)
            value = pin.get_initial_value()
            index = len(self._datas)
            self._datas.append(value)
            self._pins[pin_key] = index
            for wire_uuid in pin.wires:
                self._wires[WireKey(wire_uuid)] = index

    def __insert_input_datas(self, node_uuid: str, pins: Sequence[FlowPin]) -> None:
        for pin in pins:
            assert pin.is_data_inputs
            assert len(pin.wires) in (0, 1)

            pin_key = PinKey(node_uuid, pin.name)

            if pin.wires:
                wire_key = WireKey(pin.wires[0])
                assert wire_key in self._wires
                self._pins[pin_key] = self._wires[wire_key]
            else:
                value = pin.get_initial_value()
                index = len(self._datas)
                self._datas.append(value)
                self._pins[pin_key] = index

    def __insert_shared_variables(self, variables: Mapping[str, FlowVariable]) -> None:
        for key, val in variables.items():
            self._vars[key] = val

    @classmethod
    def from_graph(cls, graph: FlowGraph):
        result = cls()

        for key, var in graph.variables.items():
            if not var.persistent:
                var.update_value_with_initial()

        # ------------------------------------------------------------------------------
        # [IMPORTANT] The order of method calls must not change.
        for node in graph.nodes:
            result.__insert_output_datas(node.uuid, node.data_outputs)
        for node in graph.nodes:
            result.__insert_input_datas(node.uuid, node.data_inputs)
        # ------------------------------------------------------------------------------

        result.__insert_shared_variables(graph.variables.as_dict())

        return result

    @classmethod
    def from_other(cls, other, *, use_copy=False, use_deepcopy=False):
        if not isinstance(other, cls):
            raise TypeError(f"Unsupported type: {type(other).__name__}")
        if use_copy and use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist")
        if other is not None:
            if use_copy:
                return copy(other)
            elif use_deepcopy:
                return deepcopy(other)
            else:
                return other
        else:
            return cls()

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._datas = copy(self._datas)
        result._pins = copy(self._pins)
        result._wires = copy(self._wires)
        result._vars = copy(self._vars)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result._datas = deepcopy(self._datas, memo)
        result._pins = deepcopy(self._pins, memo)
        result._wires = deepcopy(self._wires, memo)
        result._vars = deepcopy(self._vars, memo)
        memo[id(self)] = result
        return result

    def copy(self):
        return self.__copy__()

    @staticmethod
    def gen_pin_key(node_uuid: str, pin_name: str):
        return PinKey(node_uuid, pin_name)

    @staticmethod
    def gen_wire_key(wire_uuid: str):
        return WireKey(wire_uuid)

    def get_pin_value(self, node_uuid: str, pin_name: str) -> Any:
        key = self.gen_pin_key(node_uuid, pin_name)
        data_index = self._pins.get(key)
        if data_index is None:
            raise KeyError(f"Not found pin value: {key}")
        return self._datas[data_index]

    def get_wire_value(self, wire_uuid: str) -> Any:
        key = self.gen_wire_key(wire_uuid)
        data_index = self._wires.get(key)
        if data_index is None:
            raise KeyError(f"Not found wire value: {wire_uuid}")
        return self._datas[data_index]

    def set_pin_value(self, node_uuid: str, pin_name: str, value: Any) -> None:
        key = self.gen_pin_key(node_uuid, pin_name)
        index = self._pins.get(key)
        if index is not None:
            self._datas[index] = value
        else:
            index = len(self._datas)
            self._datas.append(value)
            self._pins[key] = index

    def set_wire_value(self, wire_uuid: str, value: Any) -> None:
        key = self.gen_wire_key(wire_uuid)
        index = self._wires.get(key)
        if index is not None:
            self._datas[index] = value
        else:
            index = len(self._datas)
            self._datas.append(value)
            self._wires[key] = index

    def create_node_execution_record(
        self,
        index: int,
        node_uuid: str,
        pin_name: str,
        data_pins: Sequence[FlowPin],
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> NodeRecord:
        if use_copy and use_deepcopy:
            raise ValueError("'use_copy' and 'use_deepcopy' cannot coexist")

        variables = dict()
        bind_args = list()
        bind_kwargs = dict()

        for pin in data_pins:
            if not pin.is_data_action:
                raise ValueError(f"Only '{Action.data}' are allowed")

            value = self.get_pin_value(node_uuid, pin.name)
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
                        pass
                    case PinKind.exec_only:
                        assert False, "Inaccessible section"
                    case _:
                        assert False, "Inaccessible section"

        return NodeRecord(
            index=index,
            node_uuid=node_uuid,
            pin_name=pin_name,
            variables=variables,
            args=bind_args,
            kwargs=bind_kwargs,
            shared_variables=self._vars,
        )

    def update_with_node_execution_record(self, record: NodeRecord) -> None:
        for pin_name, pin_variable in record.variables.items():
            self.set_pin_value(record.node_uuid, pin_name, pin_variable)

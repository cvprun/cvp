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

ArcKey = NewType("ArcKey", str)


class PinKey(NamedTuple):
    node_uuid: str
    pin_name: str

    def __str__(self):
        return self.node_uuid + FLOW_PATH_SEPARATOR + self.pin_name


class FlowMemory:
    _datas: Deque[Any]
    _pins: Dict[PinKey, int]
    _arcs: Dict[ArcKey, int]
    _vars: Dict[str, ValueProxy]

    def __init__(self):
        self._datas = deque()
        self._pins = dict()
        self._arcs = dict()
        self._vars = dict()

    def clear(self):
        self._datas.clear()
        self._pins.clear()
        self._arcs.clear()
        self._vars.clear()

    def __insert_output_datas(self, node_uuid: str, pins: Sequence[FlowPin]) -> None:
        for pin in pins:
            assert pin.is_data_outputs
            pin_key = PinKey(node_uuid, pin.name)
            value = pin.get_initial_value()
            index = len(self._datas)
            self._datas.append(value)
            self._pins[pin_key] = index
            for arc_uuid in pin.arcs:
                self._arcs[ArcKey(arc_uuid)] = index

    def __insert_input_datas(self, node_uuid: str, pins: Sequence[FlowPin]) -> None:
        for pin in pins:
            assert pin.is_data_inputs
            assert len(pin.arcs) in (0, 1)

            pin_key = PinKey(node_uuid, pin.name)

            if pin.arcs:
                arc_key = ArcKey(pin.arcs[0])
                assert arc_key in self._arcs
                self._pins[pin_key] = self._arcs[arc_key]
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
        result._arcs = copy(self._arcs)
        result._vars = copy(self._vars)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result._datas = deepcopy(self._datas, memo)
        result._pins = deepcopy(self._pins, memo)
        result._arcs = deepcopy(self._arcs, memo)
        result._vars = deepcopy(self._vars, memo)
        memo[id(self)] = result
        return result

    def copy(self):
        return self.__copy__()

    @staticmethod
    def gen_pin_key(node_uuid: str, pin_name: str):
        return PinKey(node_uuid, pin_name)

    @staticmethod
    def gen_arc_key(arc_uuid: str):
        return ArcKey(arc_uuid)

    def get_pin_value(self, node_uuid: str, pin_name: str) -> Any:
        key = self.gen_pin_key(node_uuid, pin_name)
        data_index = self._pins.get(key)
        if data_index is None:
            raise KeyError(f"Not found pin value: {key}")
        return self._datas[data_index]

    def get_arc_value(self, arc_uuid: str) -> Any:
        key = self.gen_arc_key(arc_uuid)
        data_index = self._arcs.get(key)
        if data_index is None:
            raise KeyError(f"Not found arc value: {arc_uuid}")
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

    def set_arc_value(self, arc_uuid: str, value: Any) -> None:
        key = self.gen_arc_key(arc_uuid)
        index = self._arcs.get(key)
        if index is not None:
            self._datas[index] = value
        else:
            index = len(self._datas)
            self._datas.append(value)
            self._arcs[key] = index

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
        result_key = str()

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
                        result_key = pin.name
                    case PinKind.flow_only:
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
            result_key=result_key,
            shared_variables=self._vars,
        )

    def update_with_node_execution_record(self, record: NodeRecord) -> None:
        for pin_name, pin_variable in record.variables.items():
            self.set_pin_value(record.node_uuid, pin_name, pin_variable)

        if not record.has_exception and record.result_key:
            self.set_pin_value(record.node_uuid, record.result_key, record.result)

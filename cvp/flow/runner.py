# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Deque, Union

from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.flow.store import VariableStore
from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.special import EntrypointPin
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowRunner:
    def __init__(self, graph: FlowGraph):
        for node in graph.nodes:
            if node.template is None:
                raise ValueError(f"invalid node template: '{node.name}'")

            for pin in node.pins:
                if pin.template is None:
                    pin_path = node.name + FLOW_PATH_SEPARATOR + pin.name
                    raise ValueError(f"Invalid pin template: '{pin_path}'")

        self._graph = graph
        self._entrypoint = FlowPin.from_template(EntrypointPin())
        self._memory = VariableStore()

    def start(self, node: Union[FlowNode, str]) -> Deque[NodeExecutionRecord]:
        if isinstance(node, FlowNode):
            node_uuid = node.uuid
        elif isinstance(node, str):
            node_uuid = node
        else:
            raise TypeError(f"Invalid node type: '{type(node).__name__}'")

        start_node = self._graph.find_begin_node(node_uuid)
        if start_node is None:
            raise KeyError(f"Not found begin node: '{node_uuid}'")

        if isinstance(node, FlowNode):
            assert node == start_node

        records = Deque[NodeExecutionRecord]()
        self.run(self._entrypoint, start_node, deepcopy(self._memory), records)
        return records

    def run(
        self,
        pin: FlowPin,
        node: FlowNode,
        memory: VariableStore,
        records: Deque[NodeExecutionRecord],
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> None:
        pin_template = pin.template
        node_template = node.template
        assert pin_template is not None
        assert node_template is not None

        record = memory.create_node_execution_record(
            node_template,
            node.uuid,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
        )
        next_pin_template = node_template.run(pin_template, record)
        records.append(record)

        if next_pin_template is None:
            # Done. (No next flow)
            return

        next_pin = node.find_pin(next_pin_template.name)
        if next_pin is None:
            raise IndexError(f"Not found next pin: '{next_pin_template.name}'")

        if not next_pin.arcs:
            # Done. (Empty Arc)
            return

        if 2 <= len(next_pin.arcs):
            raise ValueError("Only one output arc is allowed")

        arc_uuid = next_pin.arcs[0]
        arc = self._graph.find_arc(arc_uuid)
        if arc is None:
            raise IndexError(f"Not found arc: '{arc_uuid}'")

        assert arc.output is not None
        assert next_pin.name == arc.output.pin.name

        input_node_uuid = arc.input.node.uuid
        input_node = self._graph.find_node(input_node_uuid)
        if input_node is None:
            raise IndexError(f"Not found input node: '{input_node_uuid}'")

        input_pin = input_node.find_pin(arc.input.pin.name)
        if input_pin is None:
            raise IndexError("Not found input pin")

        self.run(input_pin, input_node, memory, records)

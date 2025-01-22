# -*- coding: utf-8 -*-

from cvp.flow.graph import FlowGraph
from cvp.itertools.find_index import NOT_FOUND_INDEX, find_index
from cvp.memory.store import VariableStore
from cvp.nodes.node import Node
from cvp.nodes.registry.registry import NodeRegistry
from cvp.pins.pin import Pin
from cvp.pins.special import EntrypointPin


class FlowRunner:
    def __init__(self, graph: FlowGraph, node_registry: NodeRegistry):
        self._graph = graph
        self._entrypoint = EntrypointPin()
        self._node_registry = node_registry
        self._dtype_registry = node_registry.dtype_registry
        if self._dtype_registry is None:
            raise ReferenceError("The 'dtype_registry' instance has expired")

    def start(self, node_uuid: str) -> None:
        begin_node = self._graph.find_begin_node(node_uuid)
        if begin_node is None:
            raise KeyError(f"Not found begin node: '{node_uuid}'")

        memory = VariableStore()
        node = self._node_registry.get(begin_node.path)
        self.run(self._entrypoint, node, node_uuid, memory)

    def run(self, pin: Pin, node: Node, node_uuid: str, memory: VariableStore) -> None:
        record = memory.create_node_execution_record(node, node_uuid)
        next_output_pin = node.run(pin, record)

        if next_output_pin is None:
            # Done.
            return

        if not next_output_pin.arcs:
            # Done. (Empty Arc)
            return

        if 2 <= len(next_output_pin.arcs):
            raise ValueError("Only one output arc is allowed")

        arc_uuid = next_output_pin.arcs[0]
        arc = self._graph.find_arc(arc_uuid)
        if arc is None:
            raise IndexError(f"Arc {arc_uuid} could not be found")

        assert next_output_pin is not None
        assert arc is not None
        assert arc.output is not None
        assert next_output_pin.name == arc.output.pin.name

        input_node_uuid = arc.input.node.uuid
        input_node = self._node_registry.get(arc.input.node.path)
        input_pin_index = find_index(
            input_node.flow_inputs,
            key=lambda x: x.name == arc.input.pin.name,
        )
        if NOT_FOUND_INDEX == input_pin_index:
            raise IndexError(f"Not found next pin: '{arc.input.pin.name}'")

        input_pin = input_node.flow_inputs[input_pin_index]
        self.run(input_pin, input_node, input_node_uuid, memory)

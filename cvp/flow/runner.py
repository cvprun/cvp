# -*- coding: utf-8 -*-

from typing import List

from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.itertools.find_index import NOT_FOUND_INDEX, find_index
from cvp.nodes.defaults.essential.entrypoint import EntrypointNode
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.nodes.registry.registry import NodeRegistry
from cvp.pins.pin import Pin
from cvp.pins.special import EntrypointPin


class FlowRunner:
    def __init__(self, graph: FlowGraph, node_registry: NodeRegistry):
        self._graph = graph
        self._entrypoint_pin = EntrypointPin()
        self._node_registry = node_registry
        self._dtype_registry = node_registry.dtype_registry
        if self._dtype_registry is None:
            raise ReferenceError("The dtype_registry instance has expired")

    def find_entrypoint_nodes(self) -> List[FlowNode]:
        return list(filter(lambda n: isinstance(n, EntrypointNode), self._graph.nodes))

    def start(self, entrypoint_node_uuid: str):
        entrypoint_nodes = self.find_entrypoint_nodes()
        entrypoint_node_index = find_index(
            entrypoint_nodes,
            key=lambda n: n.uuid == entrypoint_node_uuid,
        )
        if NOT_FOUND_INDEX == entrypoint_node_index:
            raise IndexError(f"Not found entrypoint node: '{entrypoint_node_uuid}'")

        entrypoint_node = entrypoint_nodes[entrypoint_node_index]
        registered_node = self._node_registry.get(entrypoint_node.path)
        return self._run(self._entrypoint_pin, registered_node)

    def _run(self, pin: Pin, node: Node):
        record = NodeRecord()
        next_output_pin = node.run(pin, record)

        # flow_outputs = entrypoint_node.flow_outputs
        # pin_index = find_index(flow_outputs, lambda x: x.name == next_pin.name)
        # if NOT_FOUND_INDEX == pin_index:
        #     raise IndexError(f"Not found next pin: '{next_pin.name}'")
        # next_output_pin = flow_outputs[pin_index]

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

        input_node = self._node_registry.get(arc.input.node.path)
        input_pin_index = find_index(
            input_node.flow_inputs,
            key=lambda x: x.name == arc.input.pin.name,
        )
        if NOT_FOUND_INDEX == input_pin_index:
            raise IndexError(f"Not found next pin: '{arc.input.pin.name}'")

        input_pin = input_node.flow_inputs[input_pin_index]
        return self._run(input_pin, input_node)

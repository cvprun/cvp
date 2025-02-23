# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.pins.action import Action
from cvp.pins.stream import Stream


class GraphTestCase(TestCase):
    def test_serialize_deserialize(self):
        pin1 = FlowPin(
            name="name",
            dtype=Dtype(int),
            docs="docs",
            action=Action.flow,
            stream=Stream.output,
            required=True,
            hidden=True,
            arcs=("1", "2"),
            icon_pos=(1.0, 1.0),
            icon_size=(2.0, 2.0),
            name_pos=(3.0, 3.0),
            name_size=(4.0, 4.0),
            selected=True,
            hovering=True,
            connectable=True,
        )

        node1 = FlowNode(
            uuid="uuid",
            name="name",
            path="path",
            docs="docs",
            icon="icon",
            lock=False,
            breakpoint=False,
            hidden=False,
            color=(1.0, 0.0, 0.0, 0.0),
            flow_inputs=None,
            flow_outputs=(pin1,),
            data_inputs=None,
            data_outputs=None,
            tags=("tag1", "tag2"),
            head_height=1.0,
            flow_height=2.0,
            data_height=3.0,
            icon_pos=(11.0, 11.0),
            icon_size=(12.0, 12.0),
            name_pos=(13.0, 13.0),
            name_size=(14.0, 14.0),
            node_pos=(15.0, 15.0),
            node_size=(16.0, 16.0),
            template=None,
            selected=True,
            hovering=True,
        )

        graph1 = FlowGraph(
            uuid="uuid",
            name="name",
            docs="docs",
            icon="icon",
            lock=True,
            color=(0.0, 1.0, 0.0, 0.5),
            nodes=(node1,),
            arcs=None,
            variables=None,
            tags=("tag3", "tag4"),
        )

        serialized = serialize(graph1)
        self.assertIsInstance(serialized, dict)

        graph2 = deserialize(serialized, FlowGraph)
        self.assertIsInstance(graph2, FlowGraph)

        self.assertEqual(graph2, graph1)


if __name__ == "__main__":
    main()

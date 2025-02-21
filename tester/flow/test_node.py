# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.pins.action import Action
from cvp.pins.stream import Stream


class NodeTestCase(TestCase):
    def test_serialize_deserialize(self):
        pin1 = FlowPin(
            name="name",
            docs="docs",
            dtype="builtin.int",
            action=Action.flow,
            stream=Stream.output,
            required=True,
            hidden=True,
            arcs=("1", "2"),
            icon_pos=(1.0, 1.0),
            icon_size=(2.0, 2.0),
            name_pos=(3.0, 3.0),
            name_size=(4.0, 4.0),
            template=None,
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

        serialized = serialize(node1)
        self.assertIsInstance(serialized, dict)

        node2 = deserialize(serialized, FlowNode)
        self.assertIsInstance(node2, FlowNode)

        self.assertEqual(node2, node1)

        self.assertIsNone(node2.template)
        self.assertFalse(node2.selected)
        self.assertFalse(node2.hovering)


if __name__ == "__main__":
    main()

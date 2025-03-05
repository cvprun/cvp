# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.anchor import FlowAnchor
from cvp.flow.line_type import FlowLineType
from cvp.flow.wire import FlowWire


class WireTestCase(TestCase):
    def test_serialize_deserialize(self):
        wire1 = FlowWire(
            uuid="uuid",
            name="name",
            docs="docs",
            line_type=FlowLineType.linear,
            start_anchor=FlowAnchor(1.0, 2.0),
            end_anchor=FlowAnchor(3.0, 4.0),
            output=None,
            input=None,
            selected=True,
            hovering=True,
            polyline=((1.0, 1.0), (2.0, 2.0)),
        )

        serialized = serialize(wire1)
        self.assertIsInstance(serialized, dict)

        wire2 = deserialize(serialized, FlowWire)
        self.assertIsInstance(wire2, FlowWire)

        self.assertEqual(wire2, wire1)

        self.assertIsNone(wire2.input)
        self.assertIsNone(wire2.output)
        self.assertFalse(wire2.selected)
        self.assertFalse(wire2.hovering)
        self.assertIsInstance(wire2.polyline, list)
        self.assertFalse(wire2.polyline)


if __name__ == "__main__":
    main()

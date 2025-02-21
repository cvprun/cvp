# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.anchor import FlowAnchor
from cvp.flow.arc import FlowArc
from cvp.flow.line_type import FlowLineType


class ArcTestCase(TestCase):
    def test_serialize_deserialize(self):
        arc1 = FlowArc(
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

        serialized = serialize(arc1)
        self.assertIsInstance(serialized, dict)

        arc2 = deserialize(serialized, FlowArc)
        self.assertIsInstance(arc2, FlowArc)

        self.assertEqual(arc2, arc1)

        self.assertFalse(arc2.selected)
        self.assertFalse(arc2.hovering)


if __name__ == "__main__":
    main()

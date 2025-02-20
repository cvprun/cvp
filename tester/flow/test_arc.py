# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.anchor import FlowAnchor, FlowAnchorKeys
from cvp.flow.arc import FlowArc, FlowArcKeys
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

        arc_keys = list(FlowArcKeys)
        arc_keys.remove(FlowArcKeys.start_anchor)
        arc_keys.remove(FlowArcKeys.end_anchor)
        for key in arc_keys:
            val1 = getattr(arc1, key)
            val2 = getattr(arc2, key)
            self.assertEqual(val1, val2)

        start_anchor1 = getattr(arc1, FlowArcKeys.start_anchor)
        start_anchor2 = getattr(arc2, FlowArcKeys.start_anchor)
        end_anchor1 = getattr(arc1, FlowArcKeys.end_anchor)
        end_anchor2 = getattr(arc2, FlowArcKeys.end_anchor)
        for ak in FlowAnchorKeys:
            self.assertEqual(getattr(start_anchor1, ak), getattr(start_anchor2, ak))
            self.assertEqual(getattr(end_anchor1, ak), getattr(end_anchor2, ak))

        self.assertFalse(arc2.selected)
        self.assertFalse(arc2.hovering)


if __name__ == "__main__":
    main()

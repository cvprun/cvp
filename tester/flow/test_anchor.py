# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.anchor import FlowAnchor


class AnchorTestCase(TestCase):
    def test_serialize_deserialize(self):
        anchor1 = FlowAnchor(1.0, 2.0, selected=True, hovering=True)

        serialized = serialize(anchor1)
        self.assertIsInstance(serialized, dict)

        anchor2 = deserialize(serialized, FlowAnchor)
        self.assertIsInstance(anchor2, FlowAnchor)
        self.assertEqual(anchor2, anchor1)

        self.assertFalse(anchor2.selected)
        self.assertFalse(anchor2.hovering)


if __name__ == "__main__":
    main()

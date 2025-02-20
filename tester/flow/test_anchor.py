# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.anchor import FlowAnchor, FlowAnchorKeys


class AnchorTestCase(TestCase):
    def test_serialize_deserialize(self):
        a1 = FlowAnchor(1.0, 2.0, selected=True, hovering=True)

        serialized = serialize(a1)
        self.assertIsInstance(serialized, dict)

        a2 = deserialize(serialized, FlowAnchor)
        self.assertIsInstance(a2, FlowAnchor)

        for key in FlowAnchorKeys:
            val1 = getattr(a1, key)
            val2 = getattr(a2, key)
            self.assertEqual(val1, val2)

        self.assertFalse(a2.selected)
        self.assertFalse(a2.hovering)


if __name__ == "__main__":
    main()

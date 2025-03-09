# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.pin import FlowPin
from cvp.pins.action import Action
from cvp.pins.stream import Stream


class PinTestCase(TestCase):
    def test_serialize_deserialize(self):
        pin1 = FlowPin(
            name="name",
            dtype=Dtype(int),
            action=Action.exec,
            stream=Stream.output,
            docs="docs",
            required=True,
            hidden=True,
            wires=("1", "2"),
            icon_pos=(1.0, 1.0),
            icon_size=(2.0, 2.0),
            name_pos=(3.0, 3.0),
            name_size=(4.0, 4.0),
            selected=True,
            hovering=True,
            connectable=True,
        )

        serialized = serialize(pin1)
        self.assertIsInstance(serialized, dict)

        pin2 = deserialize(serialized, FlowPin)
        self.assertIsInstance(pin2, FlowPin)

        self.assertEqual(pin2, pin1)

        self.assertFalse(pin2.selected)
        self.assertFalse(pin2.hovering)
        self.assertFalse(pin2.connectable)


if __name__ == "__main__":
    main()

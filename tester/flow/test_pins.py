# -*- coding: utf-8 -*-

from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.pin import FlowPin
from cvp.flow.pins import FlowPins


class PinsTestCase(TestCase):
    def setUp(self):
        self.pin1 = FlowPin("pin1", Dtype(int), action="exec", stream="input")
        self.pin2 = FlowPin("pin2", Dtype(int), action="exec", stream="output")
        self.pin3 = FlowPin("pin3", Dtype(int), action="data", stream="input")
        self.pin4 = FlowPin("pin4", Dtype(int), action="data", stream="output")
        self.pins = FlowPins((self.pin1, self.pin2, self.pin3, self.pin4))

    def test_default(self):
        self.assertEqual(4, len(self.pins))

        self.assertEqual(1, len(self.pins.as_exec_inputs()))
        self.assertEqual(1, len(self.pins.as_exec_outputs()))
        self.assertEqual(1, len(self.pins.as_data_inputs()))
        self.assertEqual(1, len(self.pins.as_data_outputs()))

        self.assertEqual("pin1", self.pins.as_exec_inputs()[0].name)
        self.assertEqual("pin2", self.pins.as_exec_outputs()[0].name)
        self.assertEqual("pin3", self.pins.as_data_inputs()[0].name)
        self.assertEqual("pin4", self.pins.as_data_outputs()[0].name)

        self.assertEqual(2, len(self.pins.as_execs()))
        self.assertEqual(2, len(self.pins.as_datas()))
        self.assertEqual(2, len(self.pins.as_inputs()))
        self.assertEqual(2, len(self.pins.as_outputs()))

        self.assertEqual(1, self.pins.get_exec_lines())
        self.assertEqual(1, self.pins.get_data_lines())

        self.assertTrue(self.pins.has_exec_input())
        self.assertTrue(self.pins.has_exec_output())
        self.assertTrue(self.pins.has_data_input())
        self.assertTrue(self.pins.has_data_output())

        self.assertTrue(self.pins.is_any_exec())
        self.assertTrue(self.pins.is_any_data())
        self.assertTrue(self.pins.is_any_input())
        self.assertTrue(self.pins.is_any_output())

        self.assertFalse(self.pins.is_exec_only())
        self.assertFalse(self.pins.is_data_only())
        self.assertFalse(self.pins.is_input_only())
        self.assertFalse(self.pins.is_output_only())

        self.assertFalse(self.pins.is_begin())
        self.assertTrue(self.pins.is_middle())
        self.assertFalse(self.pins.is_end())

    def test_serialize_deserialize(self):
        serialized = serialize(self.pins)
        self.assertIsInstance(serialized, list)

        pins = deserialize(serialized, FlowPins)
        self.assertIsInstance(pins, FlowPins)

        self.assertEqual(pins, self.pins)


if __name__ == "__main__":
    main()

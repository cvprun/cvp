# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Set
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.variable import FlowVariable
from cvp.inspect.member import get_public_instance_attributes


@dataclass
class TestValue:
    value0: int = 100
    value1: str = "test"
    value2: List[int] = field(default_factory=lambda: [1, 2, 3])
    value3: Set[int] = field(default_factory=lambda: {20, 30})
    value4: Dict[int, str] = field(default_factory=lambda: {50: "value"})


class VariableTestCase(TestCase):
    def test_serialize_deserialize(self):
        name = "name"
        dtype = "dtype"
        persistent = True
        docs = "docs"
        value = TestValue()
        initial = TestValue(200, "test2")

        original = FlowVariable(
            name=name,
            dtype=dtype,
            docs=docs,
            value=value,
            initial=initial,
            persistent=persistent,
            use_copy=False,
            use_deepcopy=True,
        )

        serialized = serialize(original)
        self.assertIsInstance(serialized, dict)
        self.assertEqual(8, len(serialized))
        self.assertEqual(name, serialized[FlowVariable.Keys.name_])
        self.assertEqual(dtype, serialized[FlowVariable.Keys.dtype])
        self.assertEqual(docs, serialized[FlowVariable.Keys.docs])
        self.assertIsInstance(serialized[FlowVariable.Keys.value_], bytes)
        self.assertIsInstance(serialized[FlowVariable.Keys.initial], bytes)
        self.assertEqual(persistent, serialized[FlowVariable.Keys.persistent])
        self.assertFalse(serialized[FlowVariable.Keys.use_copy])
        self.assertTrue(serialized[FlowVariable.Keys.use_deepcopy])

        deserialized = deserialize(serialized, FlowVariable)
        self.assertIsInstance(deserialized, FlowVariable)

        lh = {key: val for key, val in get_public_instance_attributes(original)}
        rh = {key: val for key, val in get_public_instance_attributes(deserialized)}
        self.assertDictEqual(lh, rh)


if __name__ == "__main__":
    main()

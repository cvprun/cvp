# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Set
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.flow.variable import Variable
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

        original = Variable(
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
        self.assertEqual(name, serialized[Variable.Keys.name_])
        self.assertEqual(dtype, serialized[Variable.Keys.dtype])
        self.assertEqual(docs, serialized[Variable.Keys.docs])
        self.assertIsInstance(serialized[Variable.Keys.value_], bytes)
        self.assertIsInstance(serialized[Variable.Keys.initial], bytes)
        self.assertEqual(persistent, serialized[Variable.Keys.persistent])
        self.assertFalse(serialized[Variable.Keys.use_copy])
        self.assertTrue(serialized[Variable.Keys.use_deepcopy])

        deserialized = deserialize(serialized, Variable)
        self.assertIsInstance(deserialized, Variable)

        lh = {key: val for key, val in get_public_instance_attributes(original)}
        rh = {key: val for key, val in get_public_instance_attributes(deserialized)}
        self.assertDictEqual(lh, rh)


if __name__ == "__main__":
    main()

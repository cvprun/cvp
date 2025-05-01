# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Set
from unittest import TestCase, main

from type_serialize import deserialize, serialize

from cvp.dtypes.dtype import Dtype
from cvp.flow.variable import FlowVariable, VariableName


@dataclass
class _TestValue:
    value0: int = 100
    value1: str = "test"
    value2: List[int] = field(default_factory=lambda: [1, 2, 3])
    value3: Set[int] = field(default_factory=lambda: {20, 30})
    value4: Dict[int, str] = field(default_factory=lambda: {50: "value"})


class VariableTestCase(TestCase):
    def test_serialize_deserialize(self):
        name = "name"
        dtype = Dtype(int)
        persistent = True
        docs = "docs"
        value = _TestValue()
        initial = _TestValue(200, "test2")

        var1 = FlowVariable(
            name=VariableName(name),
            dtype=dtype,
            docs=docs,
            value=value,
            initial=initial,
            persistent=persistent,
            use_copy=False,
            use_deepcopy=True,
            selected=True,
            hovering=True,
        )

        serialized = serialize(var1)
        self.assertIsInstance(serialized, dict)

        var2 = deserialize(serialized, FlowVariable)
        self.assertIsInstance(var2, FlowVariable)

        self.assertEqual(var1, var2)

        self.assertFalse(var2.selected)
        self.assertFalse(var2.hovering)


if __name__ == "__main__":
    main()

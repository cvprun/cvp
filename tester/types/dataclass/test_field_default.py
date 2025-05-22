# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from unittest import TestCase, main

from cvp.types.dataclass.field_default import get_field_default
from cvp.types.dataclass.field_name import get_field_name


@dataclass
class _Val:
    key0: int = 100
    key1: int = field(default_factory=lambda: 200)


class FieldDefaultTestCase(TestCase):
    def test_default(self):
        val0 = get_field_default(_Val, get_field_name(_Val).key0)
        val1 = get_field_default(_Val, get_field_name(_Val).key1)
        self.assertEqual(100, val0)
        self.assertEqual(200, val1)


if __name__ == "__main__":
    main()

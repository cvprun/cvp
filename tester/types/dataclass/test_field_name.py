# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from unittest import TestCase, main

from cvp.types.dataclass.field_name import get_field_name


@dataclass
class _Val:
    attribute_name0: int = 100
    attribute_name1: int = field(default_factory=lambda: 200)


class FieldNameTestCase(TestCase):
    def test_instance(self):
        key = get_field_name(_Val()).attribute_name0
        self.assertIsInstance(key, str)
        self.assertEqual("attribute_name0", key)

    def test_cls(self):
        key = get_field_name(_Val).attribute_name1
        self.assertIsInstance(key, str)
        self.assertEqual("attribute_name1", key)


if __name__ == "__main__":
    main()

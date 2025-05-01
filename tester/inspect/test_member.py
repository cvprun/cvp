# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.inspect.member import get_attribute_keys


class TempAttrs:
    def __init__(self):
        self.value0 = 0
        self.value1_ = 0
        self._value2 = 0
        self._value3_ = 0
        self.__value4 = 0  # https://peps.python.org/pep-0008/#descriptive-naming-styles
        self.value5__ = 0
        self.__value6__ = 0
        self.func = abs

    @property
    def value(self):
        return self.value0

    @value.setter
    def value(self, value: int) -> None:
        self.value0 = value

    def method(self):
        pass


class MemberTestCase(TestCase):
    def test_get_attribute_keys(self):
        obj = TempAttrs()
        attrs = {key: getattr(obj, key) for key in get_attribute_keys(obj)}
        self.assertIsNotNone(attrs.pop("value0"))
        self.assertIsNotNone(attrs.pop("value1_"))
        self.assertIsNotNone(attrs.pop("_value2"))
        self.assertIsNotNone(attrs.pop("_value3_"))
        self.assertIsNotNone(attrs.pop(f"_{TempAttrs.__name__}__value4"))
        self.assertIsNotNone(attrs.pop("value5__"))
        self.assertEqual(0, len(attrs))  # It's more intuitive than `assertFalse(attrs)`


if __name__ == "__main__":
    main()

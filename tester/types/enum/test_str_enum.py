# -*- coding: utf-8 -*-

from enum import auto, unique
from unittest import TestCase, main

# noinspection PyProtectedMember
from cvp.types.enum.str_enum import _StrEnum


class StrEnumTestCase(TestCase):
    def test_auto(self):
        @unique
        class _Test1(_StrEnum):
            a = auto()
            b = auto()
            C = auto()
            D = auto()

        self.assertEqual("a", _Test1.a)
        self.assertEqual("b", _Test1.b)
        self.assertEqual("c", _Test1.C)
        self.assertEqual("d", _Test1.D)

    def test_unique(self):
        with self.assertRaises(ValueError):

            # noinspection PyUnusedLocal
            @unique
            class _Test2(_StrEnum):
                a = auto()
                b = "a"


if __name__ == "__main__":
    main()

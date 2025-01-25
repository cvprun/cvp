# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.strings.new_name import new_name


class NewNameTestCase(TestCase):
    def test_new_name(self):
        prefix = "name"
        names = list()

        name0 = new_name(prefix, names)
        names.append(name0)
        self.assertEqual(prefix, name0)
        self.assertEqual(1, len(names))

        name1 = new_name(prefix, names)
        names.append(name1)
        self.assertEqual("name (1)", name1)
        self.assertEqual(2, len(names))

        name2 = new_name(prefix, names)
        names.append(name2)
        self.assertEqual("name (2)", name2)
        self.assertEqual(3, len(names))

        name3 = new_name(prefix, names)
        names.append(name3)
        self.assertEqual("name (3)", name3)
        self.assertEqual(4, len(names))


if __name__ == "__main__":
    main()

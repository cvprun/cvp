# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.config.sections.navigation import NavigationConfig
from cvp.variables import INFINITE


class NavigationTestCase(TestCase):
    def test_category_key(self):
        config = NavigationConfig()

        expect_key0 = "tester.config.sections.test_navigation.NavigationTestCase"
        actual_key0 = config.generate_category_key(type(self))
        self.assertEqual(expect_key0, actual_key0)

        expect_key1 = "tester.config.sections.test_navigation.NavigationTestCase.Suffix"
        actual_key1 = config.generate_category_key(type(self), suffix="Suffix")
        self.assertEqual(expect_key1, actual_key1)

    def test_selected_submenu(self):
        config = NavigationConfig()

        self.assertFalse(config.has_selected_submenu(type(self)))
        self.assertFalse(config.has_selected_submenu(type(self), suffix="Suffix"))

        self.assertEqual("", config.get_selected_submenu(type(self)))
        self.assertEqual("", config.get_selected_submenu(type(self), suffix="Suffix"))

        self.assertFalse(config.has_selected_submenu(type(self)))
        self.assertFalse(config.has_selected_submenu(type(self), suffix="Suffix"))

        config.set_selected_submenu(type(self), "1")
        config.set_selected_submenu(type(self), "2", suffix="Suffix")

        self.assertTrue(config.has_selected_submenu(type(self)))
        self.assertTrue(config.has_selected_submenu(type(self), suffix="Suffix"))

        self.assertEqual("1", config.get_selected_submenu(type(self)))
        self.assertEqual("2", config.get_selected_submenu(type(self), suffix="Suffix"))

        config.clear_selected_submenu(type(self))
        config.clear_selected_submenu(type(self), suffix="Suffix")

        self.assertFalse(config.has_selected_submenu(type(self)))
        self.assertFalse(config.has_selected_submenu(type(self), suffix="Suffix"))

    def test_recent_max(self):
        config = NavigationConfig()

        self.assertEqual(INFINITE, config.get_recent_max(type(self)))
        self.assertEqual(INFINITE, config.get_recent_max(type(self), suffix="Suffix"))

        config.set_recent_max(type(self), 1)
        config.set_recent_max(type(self), 2, suffix="Suffix")

        self.assertEqual(1, config.get_recent_max(type(self)))
        self.assertEqual(2, config.get_recent_max(type(self), suffix="Suffix"))

    def test_recent_items(self):
        config = NavigationConfig()

        self.assertEqual(INFINITE, config.get_recent_max(type(self)))
        self.assertFalse(config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "A")
        self.assertListEqual(["A"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "B")
        self.assertListEqual(["A", "B"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "C")
        self.assertListEqual(["A", "B", "C"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "D")
        self.assertListEqual(["A", "B", "C", "D"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "B")
        self.assertListEqual(["A", "C", "D", "B"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "A")
        self.assertListEqual(["C", "D", "B", "A"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "A")
        self.assertListEqual(["C", "D", "B", "A"], config.get_recent_values(type(self)))

        config.set_recent_max(type(self), 2)
        self.assertListEqual(["C", "D", "B", "A"], config.get_recent_values(type(self)))

        config.add_recent_item(type(self), "E")
        self.assertListEqual(["A", "E"], config.get_recent_values(type(self)))


if __name__ == "__main__":
    main()

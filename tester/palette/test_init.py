# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.palette import (
    basic_palette,
    css4_palette,
    extended_palette,
    find_named_color,
    flat_palette,
    registered_color_count,
    registered_palette_keys,
    tableau_palette,
    vga_palette,
    xkcd_palette,
)


class ModulesTestCase(TestCase):
    def test_default(self):
        expect_names = {"basic", "css4", "extended", "flat", "tableau", "vga", "xkcd"}
        actual_names = set(registered_palette_keys())
        self.assertSetEqual(expect_names, actual_names)

    def test_basic(self):
        self.assertEqual(16, len(basic_palette()))

    def test_css4(self):
        self.assertEqual(148, len(css4_palette()))

    def test_extended(self):
        self.assertEqual(140, len(extended_palette()))

    def test_flat(self):
        self.assertEqual(240, len(flat_palette()))

    def test_tableau(self):
        self.assertEqual(10, len(tableau_palette()))

    def test_vga(self):
        self.assertEqual(16, len(vga_palette()))

    def test_xkcd(self):
        self.assertEqual(938, len(xkcd_palette()))

    def test_registered_color_count(self):
        expect_count = sum(
            (
                len(basic_palette()),
                len(css4_palette()),
                len(extended_palette()),
                len(flat_palette()),
                len(tableau_palette()),
                len(vga_palette()),
                len(xkcd_palette()),
            )
        )
        self.assertEqual(expect_count, registered_color_count())

    def test_find_named_color(self):
        from cvp.palette import basic, extended, xkcd

        self.assertTupleEqual(basic.WHITE, find_named_color("basic:white"))
        self.assertTupleEqual(xkcd.NASTY_GREEN, find_named_color("xkcd: nasty green"))
        self.assertTupleEqual(extended.BEIGE, find_named_color("extended : beige"))
        self.assertTupleEqual(extended.DIMGRAY, find_named_color(" dimgray "))


if __name__ == "__main__":
    main()

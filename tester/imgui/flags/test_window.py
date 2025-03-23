# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.imgui.flags.window import (
    BACKGROUND_FLAGS,
    NO_BRING_TO_FRONT_ON_FOCUS,
    NO_DECORATION,
    NO_FOCUS_ON_APPEARING,
    NO_MOVE,
    NO_NAV,
    NO_RESIZE,
    NO_SAVED_SETTINGS,
    NO_SCROLLBAR,
    NO_TITLE_BAR,
    NONE,
    WindowFlags,
    merge_window_flags,
)


class WindowTestCase(TestCase):
    def test_values(self):
        self.assertEqual(0b0000, NONE)
        self.assertEqual(0b0001, NO_TITLE_BAR)
        self.assertEqual(0b0010, NO_RESIZE)
        self.assertEqual(0b0100, NO_MOVE)
        self.assertEqual(0b1000, NO_SCROLLBAR)

    def test_merge_window_flags(self):
        actual_value = merge_window_flags(
            WindowFlags.none,
            WindowFlags.no_title_bar,
            WindowFlags.no_resize,
            WindowFlags.no_move,
            WindowFlags.no_scrollbar,
        )
        expect_value = NONE | NO_TITLE_BAR | NO_RESIZE | NO_MOVE | NO_SCROLLBAR

        self.assertIsInstance(actual_value, int)
        self.assertIsInstance(expect_value, int)
        self.assertEqual(actual_value, expect_value)

    def test_background_window_flags(self):
        expect_value = (
            NO_DECORATION
            | NO_DECORATION
            | NO_SAVED_SETTINGS
            | NO_FOCUS_ON_APPEARING
            | NO_BRING_TO_FRONT_ON_FOCUS
            | NO_NAV
            | NO_MOVE
        )

        self.assertIsInstance(BACKGROUND_FLAGS, int)
        self.assertIsInstance(expect_value, int)
        self.assertEqual(BACKGROUND_FLAGS, expect_value)


if __name__ == "__main__":
    main()

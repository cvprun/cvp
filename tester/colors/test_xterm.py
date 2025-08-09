# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.colors.xterm import XTERM_256COLOR_MAP


class XtermTestCase(TestCase):
    def test_default(self):
        self.assertEqual(256, len(XTERM_256COLOR_MAP))

        cs = set([c for c in XTERM_256COLOR_MAP.keys()])
        self.assertEqual(256, len(cs))
        self.assertTrue(all([0 <= c <= 255 for c in cs]))

        rs = [r for r, _, _ in XTERM_256COLOR_MAP.values()]
        gs = [g for _, g, _ in XTERM_256COLOR_MAP.values()]
        bs = [b for _, _, b in XTERM_256COLOR_MAP.values()]
        self.assertTrue(all([0 <= r <= 255 for r in rs]))
        self.assertTrue(all([0 <= g <= 255 for g in gs]))
        self.assertTrue(all([0 <= b <= 255 for b in bs]))


if __name__ == "__main__":
    main()

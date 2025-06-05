# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.values.delta import DeltaValue


class DeltaTestCase(TestCase):
    def setUp(self):
        self._current = 0
        self._previous = 0

    def _on_change(self, value: int, prev: int):
        self._current = value
        self._previous = prev

    def test_default(self):
        watcher = DeltaValue(0, 0, self._on_change)
        self.assertFalse(watcher.update(0))
        self.assertEqual(0, self._current)
        self.assertEqual(0, self._previous)
        self.assertFalse(watcher.changed)
        self.assertEqual(0, watcher.value)
        self.assertEqual(0, watcher.prev)

        self.assertTrue(watcher.update(1))
        self.assertEqual(1, self._current)
        self.assertEqual(0, self._previous)
        self.assertTrue(watcher.changed)
        self.assertEqual(1, watcher.value)
        self.assertEqual(0, watcher.prev)

        self.assertFalse(watcher.update(1))
        self.assertEqual(1, self._current)
        self.assertEqual(0, self._previous)
        self.assertFalse(watcher.changed)
        self.assertEqual(1, watcher.value)
        self.assertEqual(1, watcher.prev)

        self.assertFalse(watcher.update(1))
        self.assertEqual(1, self._current)
        self.assertEqual(0, self._previous)
        self.assertFalse(watcher.changed)
        self.assertEqual(1, watcher.value)
        self.assertEqual(1, watcher.prev)

        self.assertTrue(watcher.update(2))
        self.assertEqual(2, self._current)
        self.assertEqual(1, self._previous)
        self.assertTrue(watcher.changed)
        self.assertEqual(2, watcher.value)
        self.assertEqual(1, watcher.prev)

        self.assertFalse(watcher.update(2))
        self.assertEqual(2, self._current)
        self.assertEqual(1, self._previous)
        self.assertFalse(watcher.changed)
        self.assertEqual(2, watcher.value)
        self.assertEqual(2, watcher.prev)


if __name__ == "__main__":
    main()

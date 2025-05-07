# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.create import create_all_input_handlers
from cvp.ime.mode import InputMethodMode


class CreateTestCase(TestCase):
    def test_same_modes(self):
        handlers = create_all_input_handlers()
        modes = list(InputMethodMode)
        self.assertSetEqual(set(handlers.keys()), set(modes))


if __name__ == "__main__":
    main()

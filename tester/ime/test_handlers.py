# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.handlers import get_all_input_handler_types
from cvp.ime.mode import InputMethodMode


class CreateTestCase(TestCase):
    def test_same_modes(self):
        handlers = [ht() for ht in get_all_input_handler_types()]
        names = [h.get_method_name() for h in handlers]
        modes = list(InputMethodMode)
        self.assertSetEqual(set(names), set(modes))


if __name__ == "__main__":
    main()

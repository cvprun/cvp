# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.handlers import get_all_input_handler_types


class CreateTestCase(TestCase):
    def test_non_conflict_keys(self):
        handlers = [ht() for ht in get_all_input_handler_types()]
        names = set(h.get_method_name() for h in handlers)
        self.assertEqual(len(handlers), len(names))


if __name__ == "__main__":
    main()

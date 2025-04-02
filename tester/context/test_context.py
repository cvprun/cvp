# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.context.context import Context

# noinspection PyProtectedMember
from cvp.context.mixins._base import BaseContextMixin
from cvp.inspect.member import get_attribute_keys
from cvp.logging.disable import disable_logging


class ContextTestCase(TestCase):
    def test_home_directory(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))
            with disable_logging():
                context = Context(tmpdir)
            self.assertEqual(str(context.home), tmpdir)

    def test_attributes_keys(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))
            with disable_logging():
                context = Context(tmpdir)

            self.assertIsInstance(context, BaseContextMixin)
            member_names = list(BaseContextMixin.__annotations__.keys())
            attrs = {key: getattr(context, key) for key in get_attribute_keys(context)}
            while member_names:
                attrs.pop(member_names.pop())
            self.assertFalse(member_names)


if __name__ == "__main__":
    main()

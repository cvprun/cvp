# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.context.context import Context
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
            attrs = {key: getattr(context, key) for key in get_attribute_keys(context)}
            self.assertIsNotNone(attrs.pop("_home"))
            self.assertIsNotNone(attrs.pop("_config"))
            self.assertIsNotNone(attrs.pop("_done"))
            self.assertIsNotNone(attrs.pop("_process_manager"))
            self.assertIsNotNone(attrs.pop("_onvif_manager"))
            self.assertIsNotNone(attrs.pop("_flow_manager"))
            self.assertIsNotNone(attrs.pop("_msg_queue"))
            self.assertFalse(attrs)


if __name__ == "__main__":
    main()

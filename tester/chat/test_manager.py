# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from cvp.chat.manager import ChatManager
from cvp.resources.home import HomeDir


class ManagerTestCase(TestCase):
    def setUp(self):
        self._tmpdir = TemporaryDirectory()
        self.assertTrue(os.path.isdir(self._tmpdir.name))
        self._home = HomeDir(self._tmpdir.name)
        self._chat = ChatManager(self._home, create_tables=True)
        self.assertTrue(self._chat.database_path.exists())

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_default(self):
        self.assertEqual(1, self._chat.insert_conversation("Test"))
        a = self._chat.select_conversation_latest()


if __name__ == "__main__":
    main()

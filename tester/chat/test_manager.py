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
        conv_id = self._chat.insert_conversation("Test")
        self.assertEqual(1, conv_id)
        conv_rows = self._chat.select_conversation_latest()
        self.assertEqual(1, len(conv_rows))
        self.assertEqual(1, conv_rows[0].id)
        self.assertEqual("Test", conv_rows[0].title)

        msg_id = self._chat.insert_message(conv_id, "req", "res", "err")
        self.assertEqual(1, msg_id)
        msg_rows = self._chat.select_message_latest()
        self.assertEqual(1, len(msg_rows))
        self.assertEqual(1, msg_rows[0].id)
        self.assertEqual("req", msg_rows[0].request)
        self.assertEqual("res", msg_rows[0].response)
        self.assertEqual("err", msg_rows[0].error)


if __name__ == "__main__":
    main()

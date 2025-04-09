# -*- coding: utf-8 -*-

import os
from datetime import UTC, datetime
from tempfile import TemporaryDirectory
from time import sleep
from unittest import TestCase, main
from warnings import warn

from cvp.chat.database import ChatDatabase
from cvp.resources.home import HomeDir
from cvp.variables import DEFAULT_CHAT_LIMIT


class DatabaseTestCase(TestCase):
    def setUp(self):
        self._tmpdir = TemporaryDirectory()
        self.assertTrue(os.path.isdir(self._tmpdir.name))

        self._home = HomeDir(self._tmpdir.name)
        self._path = self._home.chat.get_database_path()
        self._chat = ChatDatabase(self._path, create_tables=True)
        self.assertTrue(self._chat.path.exists())

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_conversation(self):
        now1 = datetime.now(UTC)
        title = "Test"

        row_id = self._chat.insert_conversation(title, now1)
        self.assertEqual(1, row_id)

        rows = self._chat.select_conversation_latest()
        self.assertEqual(1, len(rows))
        self.assertEqual(row_id, rows[0].id)
        self.assertEqual(title, rows[0].title)
        self.assertEqual(now1, rows[0].created_at)
        self.assertIsNone(rows[0].updated_at)

        now2 = datetime.now(UTC)
        if now1 == now2:
            warn("Your CPU may be too fast or your datetime resolution may be low")
            sleep(1.0)
            now2 = datetime.now(UTC)

        self.assertNotEqual(now1, now2)

        updated_at = now2.isoformat()
        title2 = "Test2"
        self._chat.update_conversation_title(row_id, title2, updated_at)

        rows2 = self._chat.select_conversation_latest()
        self.assertEqual(1, len(rows2))
        self.assertEqual(row_id, rows2[0].id)
        self.assertEqual(title2, rows2[0].title)
        self.assertEqual(now1, rows2[0].created_at)
        self.assertEqual(now2, rows2[0].updated_at)

        self._chat.delete_conversation(row_id)
        rows3 = self._chat.select_conversation_latest()
        self.assertEqual(0, len(rows3))

    def test_many_conversation(self):
        limit = DEFAULT_CHAT_LIMIT

        for i in range(limit):
            self._chat.insert_conversation()

        rows1 = self._chat.select_conversation_latest()
        self.assertEqual(limit, len(rows1))
        self.assertEqual(limit, rows1[0].id)
        self.assertEqual(1, rows1[limit - 1].id)

        rows2 = self._chat.select_conversation_latest_after_id(limit)
        self.assertEqual(0, len(rows2))

        self._chat.insert_conversation()
        rows3 = self._chat.select_conversation_latest_after_id(limit)
        self.assertEqual(1, len(rows3))
        self.assertEqual(limit + 1, rows3[0].id)

    def test_message(self):
        now1 = datetime.now(UTC)

        conv_id = self._chat.insert_conversation()
        self.assertEqual(1, conv_id)

        msg_id = self._chat.insert_message(conv_id, "req", None, 0, now1)
        self.assertEqual(1, msg_id)

        rows1 = self._chat.select_message(conv_id)
        self.assertEqual(1, len(rows1))
        self.assertEqual(1, rows1[0].id)
        self.assertEqual("req", rows1[0].request)
        self.assertIsNone(rows1[0].error)
        self.assertEqual(0, rows1[0].status)
        self.assertEqual(now1, rows1[0].created_at)
        self.assertIsNone(rows1[0].updated_at)

        now2 = datetime.now(UTC)
        if now1 == now2:
            warn("Your CPU may be too fast or your datetime resolution may be low")
            sleep(1.0)
            now2 = datetime.now(UTC)

        self.assertNotEqual(now1, now2)

        updated_at = now2.isoformat()

        self._chat.update_message_error_and_status(rows1[0].id, "err", 400, updated_at)
        rows2 = self._chat.select_message(conv_id)
        self.assertEqual(1, len(rows2))
        self.assertEqual(1, rows2[0].id)
        self.assertEqual("req", rows2[0].request)
        self.assertEqual("err", rows2[0].error)
        self.assertEqual(400, rows2[0].status)
        self.assertEqual(now1, rows2[0].created_at)
        self.assertEqual(now2, rows2[0].updated_at)

        self._chat.delete_message(msg_id)
        rows3 = self._chat.select_message(conv_id)
        self.assertEqual(0, len(rows3))

    def test_stream(self):
        now1 = datetime.now(UTC)

        conv_id = self._chat.insert_conversation()
        self.assertEqual(1, conv_id)

        msg_id = self._chat.insert_message(conv_id)
        self.assertEqual(1, msg_id)

        stream_id = self._chat.insert_stream(msg_id, "data", now1)
        self.assertEqual(1, stream_id)

        rows1 = self._chat.select_stream(conv_id)
        self.assertEqual(1, len(rows1))
        self.assertEqual(1, rows1[0].id)
        self.assertEqual("data", rows1[0].chunk)
        self.assertEqual(now1, rows1[0].created_at)

        self._chat.delete_stream(stream_id)
        rows2 = self._chat.select_stream(msg_id)
        self.assertEqual(0, len(rows2))


if __name__ == "__main__":
    main()

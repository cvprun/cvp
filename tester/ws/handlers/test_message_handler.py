# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ws.handlers.message_handler import MessageHandler


class TestMessageHandler(TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            MessageHandler()  # type: ignore


if __name__ == "__main__":
    main()

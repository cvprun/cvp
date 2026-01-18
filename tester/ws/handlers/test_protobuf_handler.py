# -*- coding: utf-8 -*-

from struct import unpack
from typing import Dict, List, Optional
from unittest import TestCase, main

from cvp.ws.handlers.protobuf_handler import MSG_TYPE_MAX, MSG_TYPE_MIN, ProtobufHandler


class TestProtobufHandler(TestCase):
    def test_register_handler(self) -> None:
        handler = ProtobufHandler()
        called = []

        def msg_handler(data: bytes) -> Optional[bytes]:
            called.append(data)
            return b"response"

        handler.register(1, msg_handler)

        msg = ProtobufHandler.encode_message(1, b"test")
        response = handler.dispatch(msg)

        self.assertEqual([b"test"], called)
        self.assertEqual(b"response", response)

    def test_register_multiple_handlers(self) -> None:
        handler = ProtobufHandler()
        calls: Dict[str, List[bytes]] = {"type1": [], "type2": []}

        def handler1(data: bytes) -> Optional[bytes]:
            calls["type1"].append(data)
            return None

        def handler2(data: bytes) -> Optional[bytes]:
            calls["type2"].append(data)
            return b"type2_response"

        handler.register(1, handler1)
        handler.register(2, handler2)

        msg1 = ProtobufHandler.encode_message(1, b"hello")
        handler.dispatch(msg1)
        self.assertEqual([b"hello"], calls["type1"])
        self.assertEqual([], calls["type2"])

        msg2 = ProtobufHandler.encode_message(2, b"world")
        response = handler.dispatch(msg2)
        self.assertEqual([b"world"], calls["type2"])
        self.assertEqual(b"type2_response", response)

    def test_unregister_handler(self) -> None:
        handler = ProtobufHandler()
        called = []

        def msg_handler(data: bytes) -> Optional[bytes]:
            called.append(data)
            return None

        handler.register(1, msg_handler)
        handler.unregister(1)

        msg = ProtobufHandler.encode_message(1, b"test")
        result = handler.dispatch(msg)

        self.assertEqual([], called)
        self.assertIsNone(result)

    def test_dispatch_unknown_type(self) -> None:
        handler = ProtobufHandler()
        msg = ProtobufHandler.encode_message(999, b"test")
        result = handler.dispatch(msg)
        self.assertIsNone(result)

    def test_dispatch_invalid_data(self) -> None:
        handler = ProtobufHandler()

        result = handler.dispatch(b"")
        self.assertIsNone(result)

        result = handler.dispatch(b"\x00")
        self.assertIsNone(result)

    def test_encode_message(self) -> None:
        msg = ProtobufHandler.encode_message(0x1234, b"payload")

        msg_type = unpack(">H", msg[:2])[0]
        self.assertEqual(0x1234, msg_type)
        self.assertEqual(b"payload", msg[2:])

    def test_msg_type_validation(self) -> None:
        handler = ProtobufHandler()

        with self.assertRaises(ValueError):
            handler.register(MSG_TYPE_MIN - 1, lambda x: None)

        with self.assertRaises(ValueError):
            handler.register(MSG_TYPE_MAX + 1, lambda x: None)

    def test_on_message_delegates_to_dispatch(self) -> None:
        handler = ProtobufHandler()
        called = []

        def msg_handler(data: bytes) -> Optional[bytes]:
            called.append(data)
            return b"result"

        handler.register(1, msg_handler)
        msg = ProtobufHandler.encode_message(1, b"test")
        result = handler.on_message(msg)

        self.assertEqual([b"test"], called)
        self.assertEqual(b"result", result)


if __name__ == "__main__":
    main()

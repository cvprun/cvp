# -*- coding: utf-8 -*-

import socket
import struct
import time
from base64 import b64encode
from os import urandom
from typing import List, Optional
from unittest import TestCase, main

from cvp.ws.handlers.protobuf_handler import ProtobufHandler
from cvp.ws.threading.server import WebSocketServer


class TestWebSocketServerBinary(TestCase):
    def _create_websocket_client(self, host: str, port: int) -> socket.socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        key = b64encode(b"test-key-1234567").decode()
        request = (
            "GET / HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        client.send(request.encode())

        response = client.recv(1024)
        self.assertIn(b"101 Switching Protocols", response)

        return client

    @staticmethod
    def _encode_binary_frame(data: bytes) -> bytes:
        payload_length = len(data)

        frame = bytearray([0x82])

        if payload_length <= 125:
            frame.append(0x80 | payload_length)
        elif payload_length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", payload_length))

        masking_key = urandom(4)
        frame.extend(masking_key)

        masked_payload = bytearray(data)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    @staticmethod
    def _decode_binary_frame(data: bytes) -> bytes:
        if len(data) < 2:
            return b""

        second_byte = data[1]
        payload_length = second_byte & 0x7F

        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            payload_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            payload_start = 10
        else:
            payload_start = 2

        payload = data[payload_start : payload_start + payload_length]
        return payload

    def _encode_text_frame(self, message: str) -> bytes:
        payload = message.encode("utf-8")
        payload_length = len(payload)

        frame = bytearray([0x81])

        if payload_length <= 125:
            frame.append(0x80 | payload_length)
        elif payload_length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", payload_length))

        masking_key = urandom(4)
        frame.extend(masking_key)

        masked_payload = bytearray(payload)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    def _decode_text_frame(self, data: bytes) -> str:
        if len(data) < 2:
            return ""

        second_byte = data[1]
        payload_length = second_byte & 0x7F

        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            payload_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            payload_start = 10
        else:
            payload_start = 2

        payload = data[payload_start : payload_start + payload_length]
        return payload.decode("utf-8")

    def test_binary_handler_callback(self) -> None:
        received: List[bytes] = []

        def binary_handler(
            client_socket: socket.socket, data: bytes
        ) -> Optional[bytes]:
            received.append(data)
            return b"binary_response"

        server = WebSocketServer(
            host="localhost", port=19101, binary_handler=binary_handler
        )

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19101)
        time.sleep(0.1)

        binary_data = b"\x01\x02\x03\x04\x05"
        client.send(self._encode_binary_frame(binary_data))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_binary_frame(response)

        self.assertIn(binary_data, received)
        self.assertEqual(b"binary_response", decoded)

        client.close()
        server.stop()

    def test_message_handler_integration(self) -> None:
        received: List[bytes] = []

        class TestHandler(ProtobufHandler):
            def on_connect(self) -> None:
                pass

            def on_disconnect(self) -> None:
                pass

        handler = TestHandler()

        def msg_handler(data: bytes) -> Optional[bytes]:
            received.append(data)
            return ProtobufHandler.encode_message(2, b"response_payload")

        handler.register(1, msg_handler)

        server = WebSocketServer(host="localhost", port=19102, handler=handler)

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19102)
        time.sleep(0.1)

        msg = ProtobufHandler.encode_message(1, b"request_payload")
        client.send(self._encode_binary_frame(msg))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_binary_frame(response)

        self.assertIn(b"request_payload", received)

        resp_type = struct.unpack(">H", decoded[:2])[0]
        resp_payload = decoded[2:]
        self.assertEqual(2, resp_type)
        self.assertEqual(b"response_payload", resp_payload)

        client.close()
        server.stop()

    def test_broadcast_binary(self) -> None:
        server = WebSocketServer(host="localhost", port=19103)

        server.start()
        time.sleep(0.5)

        clients = []
        for _ in range(3):
            client = self._create_websocket_client("localhost", 19103)
            clients.append(client)

        time.sleep(0.3)
        self.assertEqual(3, server.client_count)

        broadcast_data = b"\xde\xad\xbe\xef"
        server.broadcast_binary(broadcast_data)
        time.sleep(0.1)

        for client in clients:
            response = client.recv(1024)
            decoded = self._decode_binary_frame(response)
            self.assertEqual(broadcast_data, decoded)

        for client in clients:
            client.close()

        time.sleep(0.3)
        server.stop()

    def test_mixed_text_and_binary(self) -> None:
        text_received: List[str] = []
        binary_received: List[bytes] = []

        def text_handler(client_socket: socket.socket, message: str) -> Optional[str]:
            text_received.append(message)
            return f"text_echo: {message}"

        def binary_handler(
            client_socket: socket.socket, data: bytes
        ) -> Optional[bytes]:
            binary_received.append(data)
            return b"binary_echo: " + data

        server = WebSocketServer(
            host="localhost",
            port=19104,
            message_handler=text_handler,
            binary_handler=binary_handler,
        )

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19104)
        time.sleep(0.1)

        text_msg = "hello"
        text_frame = self._encode_text_frame(text_msg)
        client.send(text_frame)
        time.sleep(0.1)
        text_response = client.recv(1024)
        text_decoded = self._decode_text_frame(text_response)
        self.assertEqual("text_echo: hello", text_decoded)

        binary_data = b"\x00\x01\x02"
        client.send(self._encode_binary_frame(binary_data))
        time.sleep(0.1)
        binary_response = client.recv(1024)
        binary_decoded = self._decode_binary_frame(binary_response)
        self.assertEqual(b"binary_echo: \x00\x01\x02", binary_decoded)

        self.assertEqual(["hello"], text_received)
        self.assertEqual([b"\x00\x01\x02"], binary_received)

        client.close()
        server.stop()


if __name__ == "__main__":
    main()

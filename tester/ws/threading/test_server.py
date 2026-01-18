# -*- coding: utf-8 -*-

import socket
import struct
import threading
import time
from base64 import b64encode
from os import urandom
from unittest import TestCase, main

from cvp.ws.threading.server import WebSocketServer


class TestWebSocketServer(TestCase):
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
    def _encode_message(message: str) -> bytes:
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

    @staticmethod
    def _decode_message(data: bytes) -> str:
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

    def test_server_start_stop(self) -> None:
        server = WebSocketServer(host="localhost", port=19001)

        server.start()
        time.sleep(0.5)

        self.assertTrue(server.is_running)
        self.assertEqual(0, server.client_count)

        server.stop()
        time.sleep(0.5)

        self.assertFalse(server.is_running)

    def test_server_client_connection(self) -> None:
        server = WebSocketServer(host="localhost", port=19002)

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19002)
        time.sleep(0.3)

        self.assertEqual(1, server.client_count)

        message = "Hello"
        client.send(self._encode_message(message))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        self.assertEqual(f"Echo: {message}", decoded)

        client.close()
        time.sleep(0.3)

        self.assertEqual(0, server.client_count)

        server.stop()

    def test_server_custom_message_handler(self) -> None:
        received_messages = []

        def custom_handler(client_socket: socket.socket, message: str) -> None:
            received_messages.append(message)
            frame = bytearray([0x81])
            payload = f"Received: {message}".encode("utf-8")
            frame.append(len(payload))
            frame.extend(payload)
            client_socket.send(bytes(frame))

        server = WebSocketServer(
            host="localhost", port=19003, message_handler=custom_handler
        )

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19003)
        time.sleep(0.1)

        client.send(self._encode_message("Test message"))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        self.assertEqual("Received: Test message", decoded)
        self.assertIn("Test message", received_messages)

        client.close()

        server.stop()

    def test_server_broadcast(self) -> None:
        server = WebSocketServer(host="localhost", port=19004)

        server.start()
        time.sleep(0.5)

        clients = []
        for _ in range(3):
            client = self._create_websocket_client("localhost", 19004)
            clients.append(client)

        time.sleep(0.3)
        self.assertEqual(3, server.client_count)

        server.broadcast("Broadcast message")
        time.sleep(0.1)

        for client in clients:
            response = client.recv(1024)
            decoded = self._decode_message(response)
            self.assertEqual("Broadcast message", decoded)

        for client in clients:
            client.close()

        time.sleep(0.3)

        server.stop()

    def test_server_multiple_messages(self) -> None:
        server = WebSocketServer(host="localhost", port=19005)

        server.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19005)
        time.sleep(0.1)

        messages = ["Message 1", "Message 2", "Message 3"]
        for msg in messages:
            client.send(self._encode_message(msg))
            time.sleep(0.1)
            response = client.recv(1024)
            decoded = self._decode_message(response)
            self.assertEqual(f"Echo: {msg}", decoded)

        client.close()

        server.stop()

    def test_server_concurrent_clients(self) -> None:
        server = WebSocketServer(host="localhost", port=19006)

        server.start()
        time.sleep(0.5)

        def client_worker(client_id: int) -> None:
            client = self._create_websocket_client("localhost", 19006)
            time.sleep(0.1)

            message = f"Client {client_id} message"
            client.send(self._encode_message(message))
            time.sleep(0.1)

            response = client.recv(1024)
            decoded = self._decode_message(response)
            self.assertEqual(f"Echo: {message}", decoded)

            client.close()

        threads = []
        for i in range(5):
            thread = threading.Thread(target=client_worker, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=5.0)

        time.sleep(0.5)

        server.stop()


if __name__ == "__main__":
    main()

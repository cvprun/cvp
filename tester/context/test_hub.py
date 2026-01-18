# -*- coding: utf-8 -*-

import socket
import struct
import time
from base64 import b64encode
from os import urandom
from unittest import TestCase, main

from cvp.context.hub import HubManager
from cvp.protos.agent_pb2 import Pat, Pit
from cvp.ws.handlers.agent_handler import MSG_TYPE_PAT, MSG_TYPE_PIT
from cvp.ws.handlers.protobuf_handler import ProtobufHandler


class TestHubManager(TestCase):
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

    def test_hub_start_stop(self) -> None:
        hub = HubManager(host="localhost", port=19301)

        self.assertFalse(hub.is_running)

        hub.start()
        time.sleep(0.5)

        self.assertTrue(hub.is_running)
        self.assertEqual(0, hub.session_count)

        hub.stop()
        time.sleep(0.5)

        self.assertFalse(hub.is_running)

    def test_hub_properties(self) -> None:
        hub = HubManager(host="127.0.0.1", port=19302)

        self.assertEqual("127.0.0.1", hub.host)
        self.assertEqual(19302, hub.port)

        hub.start()
        time.sleep(0.3)
        hub.stop()

    def test_hub_agent_connection(self) -> None:
        hub = HubManager(host="localhost", port=19303)

        hub.start()
        time.sleep(0.5)

        client = self._create_websocket_client("localhost", 19303)
        time.sleep(0.3)

        self.assertEqual(1, hub.session_count)

        pit = Pit(delay=1.0)
        pit_msg = ProtobufHandler.encode_message(MSG_TYPE_PIT, pit.SerializeToString())
        client.send(self._encode_binary_frame(pit_msg))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_binary_frame(response)

        msg_type = struct.unpack(">H", decoded[:2])[0]
        self.assertEqual(MSG_TYPE_PAT, msg_type)

        pat = Pat()
        pat.ParseFromString(decoded[2:])
        self.assertTrue(pat.ok)

        client.close()
        time.sleep(0.3)

        hub.stop()

    def test_hub_multiple_agents(self) -> None:
        hub = HubManager(host="localhost", port=19304)

        hub.start()
        time.sleep(0.5)

        clients = []
        for _ in range(3):
            client = self._create_websocket_client("localhost", 19304)
            clients.append(client)
            time.sleep(0.1)

        time.sleep(0.3)
        self.assertEqual(3, hub.session_count)

        for client in clients:
            pit = Pit(delay=0.5)
            pit_msg = ProtobufHandler.encode_message(
                MSG_TYPE_PIT, pit.SerializeToString()
            )
            client.send(self._encode_binary_frame(pit_msg))

        time.sleep(0.2)

        for client in clients:
            response = client.recv(1024)
            decoded = self._decode_binary_frame(response)
            msg_type = struct.unpack(">H", decoded[:2])[0]
            self.assertEqual(MSG_TYPE_PAT, msg_type)

        for client in clients:
            client.close()

        time.sleep(0.5)
        self.assertEqual(0, hub.session_count)

        hub.stop()


if __name__ == "__main__":
    main()

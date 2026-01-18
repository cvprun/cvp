# -*- coding: utf-8 -*-

import asyncio
import socket
import time
from typing import List, Optional
from unittest import TestCase, main

from cvp.ws.asyncio.client import WebSocketClient
from cvp.ws.handlers.protobuf_handler import ProtobufHandler
from cvp.ws.threading.server import WebSocketServer


class TestAsyncClientBinary(TestCase):
    def test_client_binary_with_server(self) -> None:
        received_on_server: List[bytes] = []

        def binary_handler(
            client_socket: socket.socket, data: bytes
        ) -> Optional[bytes]:
            received_on_server.append(data)
            return b"server_response"

        server = WebSocketServer(
            host="localhost", port=19105, binary_handler=binary_handler
        )

        server.start()
        time.sleep(0.5)

        async def run_client() -> None:
            client = WebSocketClient("ws://localhost:19105")
            await client.connect()

            await client.send_binary(b"client_binary_data")

            response = await client.receive()
            self.assertIsInstance(response, bytes)
            self.assertEqual(b"server_response", response)

            await client.disconnect()

        asyncio.run(run_client())

        self.assertIn(b"client_binary_data", received_on_server)

        server.stop()

    def test_client_with_protobuf_handler(self) -> None:
        server_received: List[bytes] = []

        class ServerHandler(ProtobufHandler):
            def on_connect(self) -> None:
                pass

            def on_disconnect(self) -> None:
                pass

        server_handler = ServerHandler()

        def server_msg_handler(data: bytes) -> Optional[bytes]:
            server_received.append(data)
            return ProtobufHandler.encode_message(2, b"server_reply")

        server_handler.register(1, server_msg_handler)

        server = WebSocketServer(host="localhost", port=19106, handler=server_handler)

        server.start()
        time.sleep(0.5)

        client_received: List[bytes] = []

        class ClientHandler(ProtobufHandler):
            def on_connect(self) -> None:
                pass

            def on_disconnect(self) -> None:
                pass

        client_handler = ClientHandler()

        def client_msg_handler(data: bytes) -> Optional[bytes]:
            client_received.append(data)
            return None

        client_handler.register(2, client_msg_handler)

        async def run_client() -> None:
            client = WebSocketClient("ws://localhost:19106", handler=client_handler)
            await client.connect()

            msg = ProtobufHandler.encode_message(1, b"client_request")
            await client.send_binary(msg)

            response = await client.receive()
            self.assertIsInstance(response, bytes)
            assert isinstance(response, bytes)
            await client.on_binary_message(response)

            await client.disconnect()

        asyncio.run(run_client())

        self.assertIn(b"client_request", server_received)
        self.assertIn(b"server_reply", client_received)

        server.stop()


if __name__ == "__main__":
    main()

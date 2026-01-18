# -*- coding: utf-8 -*-

import asyncio
from unittest import TestCase, main

import websockets

from cvp.ws.asyncio.client import WebSocketClient


class TestWebSocketClient(TestCase):
    def test_client_connect_disconnect(self) -> None:
        async def run_test() -> None:
            async def echo_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")

            server = await websockets.serve(echo_handler, "localhost", 18770)

            try:
                client = WebSocketClient("ws://localhost:18770")
                await client.connect()

                self.assertTrue(client.is_connected)

                await client.disconnect()

                self.assertFalse(client.is_connected)

            finally:
                server.close()
                await server.wait_closed()

        asyncio.run(run_test())

    def test_client_send_receive(self) -> None:
        async def run_test() -> None:
            async def echo_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")

            server = await websockets.serve(echo_handler, "localhost", 18771)

            try:
                client = WebSocketClient("ws://localhost:18771")
                await client.connect()

                await client.send("Hello Server")
                response = await client.receive()
                self.assertEqual("Echo: Hello Server", response)

                await client.disconnect()

            finally:
                server.close()
                await server.wait_closed()

        asyncio.run(run_test())

    def test_client_message_handler(self) -> None:
        received_messages = []

        async def run_test() -> None:
            async def echo_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")

            server = await websockets.serve(echo_handler, "localhost", 18772)

            try:

                class CustomClient(WebSocketClient):
                    async def on_message(self, message: str) -> None:
                        received_messages.append(message)

                client = CustomClient("ws://localhost:18772")

                client_task = asyncio.create_task(client.start())

                await asyncio.sleep(0.5)

                self.assertTrue(client.is_connected)

                await client.send("Test message")

                await asyncio.sleep(0.5)

                self.assertGreater(len(received_messages), 0)
                self.assertIn("Echo: Test message", received_messages)

                await client.stop()
                client_task.cancel()

                try:
                    await client_task
                except asyncio.CancelledError:
                    pass

            finally:
                server.close()
                await server.wait_closed()

        asyncio.run(run_test())

    def test_client_reconnect(self) -> None:
        async def run_test() -> None:
            async def echo_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")

            server = await websockets.serve(echo_handler, "localhost", 18773)

            try:
                client = WebSocketClient("ws://localhost:18773", reconnect_interval=0.5)

                client_task = asyncio.create_task(client.start())

                await asyncio.sleep(0.5)
                self.assertTrue(client.is_connected)

                if client._ws:
                    await client._ws.close()

                await asyncio.sleep(1.5)

                self.assertTrue(client.is_connected)

                await client.stop()
                client_task.cancel()

                try:
                    await client_task
                except asyncio.CancelledError:
                    pass

            finally:
                server.close()
                await server.wait_closed()

        asyncio.run(run_test())

    def test_client_multiple_messages(self) -> None:
        async def run_test() -> None:
            async def echo_handler(websocket):
                async for message in websocket:
                    await websocket.send(f"Echo: {message}")

            server = await websockets.serve(echo_handler, "localhost", 18774)

            try:
                client = WebSocketClient("ws://localhost:18774")
                await client.connect()

                messages = ["Message 1", "Message 2", "Message 3"]
                for msg in messages:
                    await client.send(msg)
                    response = await client.receive()
                    self.assertEqual(f"Echo: {msg}", response)

                await client.disconnect()

            finally:
                server.close()
                await server.wait_closed()

        asyncio.run(run_test())


if __name__ == "__main__":
    main()

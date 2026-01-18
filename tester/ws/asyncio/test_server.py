# -*- coding: utf-8 -*-

import asyncio
from unittest import TestCase, main

import websockets

from cvp.ws.asyncio.server import WebSocketServer


class TestWebSocketServer(TestCase):
    def test_server_start_stop(self) -> None:
        async def run_test() -> None:
            server = WebSocketServer(host="localhost", port=18765)

            server_task = asyncio.create_task(server.start())

            await asyncio.sleep(0.5)

            self.assertTrue(server.is_running)
            self.assertEqual(0, server.client_count)

            await server.stop()
            server_task.cancel()

            try:
                await server_task
            except asyncio.CancelledError:
                pass

            self.assertFalse(server.is_running)

        asyncio.run(run_test())

    def test_server_client_connection(self) -> None:
        async def run_test() -> None:
            server = WebSocketServer(host="localhost", port=18766)

            server_task = asyncio.create_task(server.start())
            await asyncio.sleep(0.5)

            async with websockets.connect("ws://localhost:18766") as ws:
                self.assertEqual(1, server.client_count)

                await ws.send("Hello")
                response = await ws.recv()
                self.assertEqual("Echo: Hello", response)

            await asyncio.sleep(0.1)
            self.assertEqual(0, server.client_count)

            await server.stop()
            server_task.cancel()

            try:
                await server_task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())

    def test_server_custom_message_handler(self) -> None:
        received_messages = []

        async def custom_handler(websocket, message):
            received_messages.append(message)
            await websocket.send(f"Received: {message}")

        async def run_test() -> None:
            server = WebSocketServer(
                host="localhost", port=18767, message_handler=custom_handler
            )

            server_task = asyncio.create_task(server.start())
            await asyncio.sleep(0.5)

            async with websockets.connect("ws://localhost:18767") as ws:
                await ws.send("Test message")
                response = await ws.recv()
                self.assertEqual("Received: Test message", response)

            self.assertIn("Test message", received_messages)

            await server.stop()
            server_task.cancel()

            try:
                await server_task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())

    def test_server_broadcast(self) -> None:
        async def run_test() -> None:
            server = WebSocketServer(host="localhost", port=18768)

            server_task = asyncio.create_task(server.start())
            await asyncio.sleep(0.5)

            clients = []
            for _ in range(3):
                client = await websockets.connect("ws://localhost:18768")
                clients.append(client)

            await asyncio.sleep(0.1)
            self.assertEqual(3, server.client_count)

            await server.broadcast("Broadcast message")

            for client in clients:
                message = await client.recv()
                self.assertEqual("Broadcast message", message)

            for client in clients:
                await client.close()

            await asyncio.sleep(0.1)

            await server.stop()
            server_task.cancel()

            try:
                await server_task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())

    def test_server_multiple_messages(self) -> None:
        async def run_test() -> None:
            server = WebSocketServer(host="localhost", port=18769)

            server_task = asyncio.create_task(server.start())
            await asyncio.sleep(0.5)

            async with websockets.connect("ws://localhost:18769") as ws:
                messages = ["Message 1", "Message 2", "Message 3"]
                for msg in messages:
                    await ws.send(msg)
                    response = await ws.recv()
                    self.assertEqual(f"Echo: {msg}", response)

            await server.stop()
            server_task.cancel()

            try:
                await server_task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())


if __name__ == "__main__":
    main()

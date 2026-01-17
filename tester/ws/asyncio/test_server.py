# -*- coding: utf-8 -*-

import asyncio

import pytest
import websockets

from cvp.ws.asyncio.server import WebSocketServer


class TestWebSocketServer:
    """Tests for asyncio-based WebSocket server"""

    @pytest.mark.asyncio
    async def test_server_start_stop(self):
        """Test server start and stop"""
        server = WebSocketServer(host="localhost", port=18765)

        # Start server (background)
        server_task = asyncio.create_task(server.start())

        # Wait for server to start
        await asyncio.sleep(0.5)

        assert server.is_running
        assert server.client_count == 0

        # Stop server
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

        assert not server.is_running

    @pytest.mark.asyncio
    async def test_server_client_connection(self):
        """Test client connection"""
        server = WebSocketServer(host="localhost", port=18766)

        # Start server
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # Connect client
        async with websockets.connect("ws://localhost:18766") as ws:
            assert server.client_count == 1

            # Send and receive message (echo server)
            await ws.send("Hello")
            response = await ws.recv()
            assert response == "Echo: Hello"

        # Verify client count after disconnection
        await asyncio.sleep(0.1)
        assert server.client_count == 0

        # Stop server
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_custom_message_handler(self):
        """Test custom message handler"""
        received_messages = []

        async def custom_handler(websocket, message):
            received_messages.append(message)
            await websocket.send(f"Received: {message}")

        server = WebSocketServer(
            host="localhost", port=18767, message_handler=custom_handler
        )

        # Start server
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # Connect client and send message
        async with websockets.connect("ws://localhost:18767") as ws:
            await ws.send("Test message")
            response = await ws.recv()
            assert response == "Received: Test message"

        assert "Test message" in received_messages

        # Stop server
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_broadcast(self):
        """Test broadcast"""
        server = WebSocketServer(host="localhost", port=18768)

        # Start server
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # Connect multiple clients
        clients = []
        for _ in range(3):
            client = await websockets.connect("ws://localhost:18768")
            clients.append(client)

        await asyncio.sleep(0.1)
        assert server.client_count == 3

        # Broadcast
        await server.broadcast("Broadcast message")

        # Verify all clients received the message
        for client in clients:
            message = await client.recv()
            assert message == "Broadcast message"

        # Disconnect clients
        for client in clients:
            await client.close()

        await asyncio.sleep(0.1)

        # Stop server
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_multiple_messages(self):
        """Test multiple message send and receive"""
        server = WebSocketServer(host="localhost", port=18769)

        # Start server
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # Connect client
        async with websockets.connect("ws://localhost:18769") as ws:
            # Send multiple messages
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                await ws.send(msg)
                response = await ws.recv()
                assert response == f"Echo: {msg}"

        # Stop server
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

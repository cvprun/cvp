# -*- coding: utf-8 -*-

import asyncio

import pytest
import websockets

from cvp.ws.asyncio.client import WebSocketClient


class TestWebSocketClient:
    """Tests for asyncio-based WebSocket client"""

    @pytest.mark.asyncio
    async def test_client_connect_disconnect(self):
        """Test client connection and disconnection"""

        # Start test server
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18770)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:18770")
            await client.connect()

            assert client.is_connected

            # Disconnect
            await client.disconnect()

            assert not client.is_connected

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_send_receive(self):
        """Test client message send and receive"""

        # Start test server
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18771)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:18771")
            await client.connect()

            # Send and receive message
            await client.send("Hello Server")
            response = await client.receive()
            assert response == "Echo: Hello Server"

            # Disconnect
            await client.disconnect()

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_message_handler(self):
        """Test client message handler"""
        received_messages = []

        # Start test server
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18772)

        try:
            # Create client with custom message handler
            class CustomClient(WebSocketClient):
                async def on_message(self, message: str) -> None:
                    received_messages.append(message)

            client = CustomClient("ws://localhost:18772")

            # Run start() as background task since it's an infinite loop
            client_task = asyncio.create_task(client.start())

            # Wait for client to connect
            await asyncio.sleep(0.5)

            assert client.is_connected

            # Send message
            await client.send("Test message")

            # Wait for message to be received
            await asyncio.sleep(0.5)

            assert len(received_messages) > 0
            assert "Echo: Test message" in received_messages

            # Stop client
            await client.stop()
            client_task.cancel()

            try:
                await client_task
            except asyncio.CancelledError:
                pass

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_reconnect(self):
        """Test client reconnection"""

        # Start test server
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18773)

        try:
            # Set short interval for fast reconnection
            client = WebSocketClient("ws://localhost:18773", reconnect_interval=0.5)

            # Start client (background)
            client_task = asyncio.create_task(client.start())

            # Wait for connection
            await asyncio.sleep(0.5)
            assert client.is_connected

            # Force disconnect
            if client._ws:
                await client._ws.close()

            # Wait for reconnection
            await asyncio.sleep(1.5)

            # Verify reconnection
            assert client.is_connected

            # Stop client
            await client.stop()
            client_task.cancel()

            try:
                await client_task
            except asyncio.CancelledError:
                pass

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_multiple_messages(self):
        """Test multiple message send and receive"""

        # Start test server
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18774)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:18774")
            await client.connect()

            # Send and receive multiple messages
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                await client.send(msg)
                response = await client.receive()
                assert response == f"Echo: {msg}"

            # Disconnect
            await client.disconnect()

        finally:
            server.close()
            await server.wait_closed()

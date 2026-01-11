# -*- coding: utf-8 -*-

import asyncio

import pytest
import websockets

from cvp.ws.asyncio.server import WebSocketServer


class TestWebSocketServer:
    """asyncio 기반 WebSocket 서버 테스트"""

    @pytest.mark.asyncio
    async def test_server_start_stop(self):
        """서버 시작 및 중지 테스트"""
        server = WebSocketServer(host="localhost", port=18765)

        # 서버 시작 (백그라운드로)
        server_task = asyncio.create_task(server.start())

        # 서버가 시작될 때까지 대기
        await asyncio.sleep(0.5)

        assert server.is_running
        assert server.client_count == 0

        # 서버 중지
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

        assert not server.is_running

    @pytest.mark.asyncio
    async def test_server_client_connection(self):
        """클라이언트 연결 테스트"""
        server = WebSocketServer(host="localhost", port=18766)

        # 서버 시작
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # 클라이언트 연결
        async with websockets.connect("ws://localhost:18766") as ws:
            assert server.client_count == 1

            # 메시지 전송 및 수신 (에코 서버)
            await ws.send("Hello")
            response = await ws.recv()
            assert response == "Echo: Hello"

        # 연결 종료 후 클라이언트 수 확인
        await asyncio.sleep(0.1)
        assert server.client_count == 0

        # 서버 중지
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_custom_message_handler(self):
        """커스텀 메시지 핸들러 테스트"""
        received_messages = []

        async def custom_handler(websocket, message):
            received_messages.append(message)
            await websocket.send(f"Received: {message}")

        server = WebSocketServer(
            host="localhost", port=18767, message_handler=custom_handler
        )

        # 서버 시작
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # 클라이언트 연결 및 메시지 전송
        async with websockets.connect("ws://localhost:18767") as ws:
            await ws.send("Test message")
            response = await ws.recv()
            assert response == "Received: Test message"

        assert "Test message" in received_messages

        # 서버 중지
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_broadcast(self):
        """브로드캐스트 테스트"""
        server = WebSocketServer(host="localhost", port=18768)

        # 서버 시작
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # 여러 클라이언트 연결
        clients = []
        for _ in range(3):
            client = await websockets.connect("ws://localhost:18768")
            clients.append(client)

        await asyncio.sleep(0.1)
        assert server.client_count == 3

        # 브로드캐스트
        await server.broadcast("Broadcast message")

        # 모든 클라이언트가 메시지 수신 확인
        for client in clients:
            message = await client.recv()
            assert message == "Broadcast message"

        # 클라이언트 연결 종료
        for client in clients:
            await client.close()

        await asyncio.sleep(0.1)

        # 서버 중지
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_server_multiple_messages(self):
        """여러 메시지 송수신 테스트"""
        server = WebSocketServer(host="localhost", port=18769)

        # 서버 시작
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(0.5)

        # 클라이언트 연결
        async with websockets.connect("ws://localhost:18769") as ws:
            # 여러 메시지 전송
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                await ws.send(msg)
                response = await ws.recv()
                assert response == f"Echo: {msg}"

        # 서버 중지
        await server.stop()
        server_task.cancel()

        try:
            await server_task
        except asyncio.CancelledError:
            pass

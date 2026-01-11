# -*- coding: utf-8 -*-

import asyncio

import pytest
import websockets

from cvp.ws.asyncio.client import WebSocketClient


class TestWebSocketClient:
    """asyncio 기반 WebSocket 클라이언트 테스트"""

    @pytest.mark.asyncio
    async def test_client_connect_disconnect(self):
        """클라이언트 연결 및 종료 테스트"""

        # 테스트용 서버 시작
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18770)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:18770")
            await client.connect()

            assert client.is_connected

            # 연결 종료
            await client.disconnect()

            assert not client.is_connected

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_send_receive(self):
        """클라이언트 메시지 송수신 테스트"""

        # 테스트용 서버 시작
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18771)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:18771")
            await client.connect()

            # 메시지 전송 및 수신
            await client.send("Hello Server")
            response = await client.receive()
            assert response == "Echo: Hello Server"

            # 연결 종료
            await client.disconnect()

        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_client_message_handler(self):
        """클라이언트 메시지 핸들러 테스트"""
        received_messages = []

        # 테스트용 서버 시작
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18772)

        try:
            # 커스텀 메시지 핸들러를 가진 클라이언트 생성
            class CustomClient(WebSocketClient):
                async def on_message(self, message: str) -> None:
                    received_messages.append(message)

            client = CustomClient("ws://localhost:18772")

            # start() 메서드는 무한 루프이므로 백그라운드 태스크로 실행
            client_task = asyncio.create_task(client.start())

            # 클라이언트가 연결될 때까지 대기
            await asyncio.sleep(0.5)

            assert client.is_connected

            # 메시지 전송
            await client.send("Test message")

            # 메시지가 수신될 때까지 대기
            await asyncio.sleep(0.5)

            assert len(received_messages) > 0
            assert "Echo: Test message" in received_messages

            # 클라이언트 중지
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
        """클라이언트 재연결 테스트"""

        # 테스트용 서버 시작
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18773)

        try:
            # 빠른 재연결을 위해 interval을 짧게 설정
            client = WebSocketClient("ws://localhost:18773", reconnect_interval=0.5)

            # 클라이언트 시작 (백그라운드)
            client_task = asyncio.create_task(client.start())

            # 연결 대기
            await asyncio.sleep(0.5)
            assert client.is_connected

            # 강제로 연결 종료
            if client._ws:
                await client._ws.close()

            # 재연결 대기
            await asyncio.sleep(1.5)

            # 재연결 확인
            assert client.is_connected

            # 클라이언트 중지
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
        """여러 메시지 송수신 테스트"""

        # 테스트용 서버 시작
        async def echo_handler(websocket):
            async for message in websocket:
                await websocket.send(f"Echo: {message}")

        server = await websockets.serve(echo_handler, "localhost", 18774)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:18774")
            await client.connect()

            # 여러 메시지 전송 및 수신
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                await client.send(msg)
                response = await client.receive()
                assert response == f"Echo: {msg}"

            # 연결 종료
            await client.disconnect()

        finally:
            server.close()
            await server.wait_closed()

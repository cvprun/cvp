# -*- coding: utf-8 -*-

import socket
import struct
import threading
import time
from base64 import b64encode
from hashlib import sha1

from cvp.ws.threading.client import WebSocketClient


class SimpleWebSocketServer:
    """테스트용 간단한 WebSocket 서버"""

    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None

    def _perform_handshake(self, client_socket: socket.socket) -> bool:
        """WebSocket 핸드셰이크 수행"""
        try:
            request = client_socket.recv(1024).decode("utf-8")
            headers: dict[str, str] = {}
            lines = request.split("\r\n")
            for line in lines[1:]:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    headers[k] = v

            ws_key = headers.get("Sec-WebSocket-Key")
            if not ws_key:
                return False

            accept_key = b64encode(
                sha1((ws_key + self.MAGIC_STRING).encode()).digest()
            ).decode()

            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n"
                "\r\n"
            )
            client_socket.send(response.encode())
            return True
        except Exception:
            return False

    def _decode_frame(self, data: bytes) -> str:
        """WebSocket 프레임 디코딩"""
        if len(data) < 2:
            return ""

        second_byte = data[1]
        payload_length = second_byte & 0x7F

        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            mask_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            mask_start = 10
        else:
            mask_start = 2

        masking_key = data[mask_start : mask_start + 4]
        payload_start = mask_start + 4

        payload = bytearray(data[payload_start : payload_start + payload_length])
        for i in range(len(payload)):
            payload[i] ^= masking_key[i % 4]

        return payload.decode("utf-8")

    def _encode_frame(self, message: str) -> bytes:
        """WebSocket 프레임 인코딩"""
        payload = message.encode("utf-8")
        payload_length = len(payload)

        frame = bytearray([0x81])  # FIN=1, opcode=1

        if payload_length <= 125:
            frame.append(payload_length)
        elif payload_length <= 65535:
            frame.append(126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(127)
            frame.extend(struct.pack(">Q", payload_length))

        frame.extend(payload)
        return bytes(frame)

    def _handle_client(self, client_socket: socket.socket):
        """클라이언트 핸들링"""
        if not self._perform_handshake(client_socket):
            client_socket.close()
            return

        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break

                message = self._decode_frame(data)
                if message:
                    # 에코 응답
                    response = self._encode_frame(f"Echo: {message}")
                    client_socket.send(response)
        except Exception:
            pass
        finally:
            client_socket.close()

    def _accept_loop(self):
        """클라이언트 연결 수락 루프"""
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client, args=(client_socket,), daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except Exception:
                break

    def start(self):
        """서버 시작"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1.0)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.thread = threading.Thread(target=self._accept_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """서버 중지"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join(timeout=2.0)


class TestWebSocketClient:
    """threading 기반 WebSocket 클라이언트 테스트"""

    def test_client_connect_disconnect(self):
        """클라이언트 연결 및 종료 테스트"""
        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19101)
        server.start()
        time.sleep(0.5)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:19101")
            success = client.connect()

            assert success
            assert client.is_connected

            # 연결 종료
            client.disconnect()

            assert not client.is_connected

        finally:
            server.stop()

    def test_client_send_receive(self):
        """클라이언트 메시지 송수신 테스트"""
        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19102)
        server.start()
        time.sleep(0.5)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:19102")
            client.connect()

            # 메시지 전송
            success = client.send("Hello Server")
            assert success

            time.sleep(0.1)

            # 연결 종료
            client.disconnect()

        finally:
            server.stop()

    def test_client_message_handler(self):
        """클라이언트 메시지 핸들러 테스트"""
        received_messages = []

        def message_handler(message: str):
            received_messages.append(message)

        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19103)
        server.start()
        time.sleep(0.5)

        try:
            # 클라이언트 생성 및 시작
            client = WebSocketClient(
                "ws://localhost:19103", message_handler=message_handler
            )
            client.start()

            # 연결 대기
            time.sleep(0.5)
            assert client.is_connected

            # 메시지 전송
            client.send("Test message")

            # 응답 대기
            time.sleep(0.5)

            assert len(received_messages) > 0
            assert "Echo: Test message" in received_messages

            # 클라이언트 중지
            client.stop()

        finally:
            server.stop()

    def test_client_reconnect(self):
        """클라이언트 재연결 테스트"""
        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19104)
        server.start()
        time.sleep(0.5)

        try:
            # 빠른 재연결을 위해 interval을 짧게 설정
            client = WebSocketClient("ws://localhost:19104", reconnect_interval=0.5)
            client.start()

            # 연결 대기
            time.sleep(0.5)
            assert client.is_connected

            # 강제로 연결 종료
            if client._socket:
                client._socket.close()
                client._connected = False

            # 재연결 대기
            time.sleep(1.5)

            # 재연결 확인
            assert client.is_connected

            # 클라이언트 중지
            client.stop()

        finally:
            server.stop()

    def test_client_multiple_messages(self):
        """여러 메시지 송수신 테스트"""
        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19105)
        server.start()
        time.sleep(0.5)

        try:
            # 클라이언트 생성 및 연결
            client = WebSocketClient("ws://localhost:19105")
            client.connect()

            # 여러 메시지 전송
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                success = client.send(msg)
                assert success
                time.sleep(0.1)

            # 연결 종료
            client.disconnect()

        finally:
            server.stop()

    def test_client_auto_start_with_reconnect(self):
        """자동 시작 및 재연결 테스트"""
        # 테스트용 서버 시작
        server = SimpleWebSocketServer("localhost", 19106)
        server.start()
        time.sleep(0.5)

        try:
            received_messages = []

            def message_handler(message: str):
                received_messages.append(message)

            # 클라이언트 자동 시작
            client = WebSocketClient(
                "ws://localhost:19106",
                reconnect_interval=0.5,
                message_handler=message_handler,
            )
            client.start()

            # 연결 대기
            time.sleep(0.5)
            assert client.is_connected
            assert client.is_running

            # 메시지 전송 및 수신
            client.send("Auto test")
            time.sleep(0.5)

            assert len(received_messages) > 0

            # 클라이언트 중지
            client.stop()

            assert not client.is_running

        finally:
            server.stop()

    def test_client_connection_failure(self):
        """연결 실패 테스트"""
        # 서버 없이 연결 시도
        client = WebSocketClient("ws://localhost:19999")
        success = client.connect()

        assert not success
        assert not client.is_connected

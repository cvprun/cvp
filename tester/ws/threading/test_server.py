# -*- coding: utf-8 -*-

import socket
import threading
import time
from base64 import b64encode

from cvp.ws.threading.server import WebSocketServer


class TestWebSocketServer:
    """threading 기반 WebSocket 서버 테스트"""

    def _create_websocket_client(self, host: str, port: int) -> socket.socket:
        """WebSocket 클라이언트 소켓 생성 및 핸드셰이크"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # WebSocket 핸드셰이크
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

        # 핸드셰이크 응답 수신
        response = client.recv(1024)
        assert b"101 Switching Protocols" in response

        return client

    def _encode_message(self, message: str) -> bytes:
        """WebSocket 프레임 인코딩 (클라이언트 -> 서버)"""
        import struct
        from os import urandom

        payload = message.encode("utf-8")
        payload_length = len(payload)

        frame = bytearray([0x81])  # FIN=1, opcode=1 (text)

        if payload_length <= 125:
            frame.append(0x80 | payload_length)  # MASK=1
        elif payload_length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", payload_length))

        # 마스킹 키
        masking_key = urandom(4)
        frame.extend(masking_key)

        # 페이로드 마스킹
        masked_payload = bytearray(payload)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    def _decode_message(self, data: bytes) -> str:
        """WebSocket 프레임 디코딩 (서버 -> 클라이언트)"""
        import struct

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

    def test_server_start_stop(self):
        """서버 시작 및 중지 테스트"""
        server = WebSocketServer(host="localhost", port=19001)

        # 서버 시작
        server.start()
        time.sleep(0.5)

        assert server.is_running
        assert server.client_count == 0

        # 서버 중지
        server.stop()
        time.sleep(0.5)

        assert not server.is_running

    def test_server_client_connection(self):
        """클라이언트 연결 테스트"""
        server = WebSocketServer(host="localhost", port=19002)

        # 서버 시작
        server.start()
        time.sleep(0.5)

        # 클라이언트 연결
        client = self._create_websocket_client("localhost", 19002)
        time.sleep(0.3)

        assert server.client_count == 1

        # 메시지 전송 및 수신 (에코 서버)
        message = "Hello"
        client.send(self._encode_message(message))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        assert decoded == f"Echo: {message}"

        # 클라이언트 종료
        client.close()
        time.sleep(0.3)

        assert server.client_count == 0

        # 서버 중지
        server.stop()

    def test_server_custom_message_handler(self):
        """커스텀 메시지 핸들러 테스트"""
        received_messages = []

        def custom_handler(client_socket: socket.socket, message: str):
            received_messages.append(message)
            # 응답 전송
            frame = bytearray([0x81])  # FIN=1, opcode=1
            payload = f"Received: {message}".encode("utf-8")
            frame.append(len(payload))
            frame.extend(payload)
            client_socket.send(bytes(frame))

        server = WebSocketServer(
            host="localhost", port=19003, message_handler=custom_handler
        )

        # 서버 시작
        server.start()
        time.sleep(0.5)

        # 클라이언트 연결 및 메시지 전송
        client = self._create_websocket_client("localhost", 19003)
        time.sleep(0.1)

        client.send(self._encode_message("Test message"))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        assert decoded == "Received: Test message"
        assert "Test message" in received_messages

        # 클라이언트 종료
        client.close()

        # 서버 중지
        server.stop()

    def test_server_broadcast(self):
        """브로드캐스트 테스트"""
        server = WebSocketServer(host="localhost", port=19004)

        # 서버 시작
        server.start()
        time.sleep(0.5)

        # 여러 클라이언트 연결
        clients = []
        for _ in range(3):
            client = self._create_websocket_client("localhost", 19004)
            clients.append(client)

        time.sleep(0.3)
        assert server.client_count == 3

        # 브로드캐스트
        server.broadcast("Broadcast message")
        time.sleep(0.1)

        # 모든 클라이언트가 메시지 수신 확인
        for client in clients:
            response = client.recv(1024)
            decoded = self._decode_message(response)
            assert decoded == "Broadcast message"

        # 클라이언트 연결 종료
        for client in clients:
            client.close()

        time.sleep(0.3)

        # 서버 중지
        server.stop()

    def test_server_multiple_messages(self):
        """여러 메시지 송수신 테스트"""
        server = WebSocketServer(host="localhost", port=19005)

        # 서버 시작
        server.start()
        time.sleep(0.5)

        # 클라이언트 연결
        client = self._create_websocket_client("localhost", 19005)
        time.sleep(0.1)

        # 여러 메시지 전송
        messages = ["Message 1", "Message 2", "Message 3"]
        for msg in messages:
            client.send(self._encode_message(msg))
            time.sleep(0.1)
            response = client.recv(1024)
            decoded = self._decode_message(response)
            assert decoded == f"Echo: {msg}"

        # 클라이언트 종료
        client.close()

        # 서버 중지
        server.stop()

    def test_server_concurrent_clients(self):
        """동시 다중 클라이언트 테스트"""
        server = WebSocketServer(host="localhost", port=19006)

        # 서버 시작
        server.start()
        time.sleep(0.5)

        # 여러 클라이언트가 동시에 메시지 전송
        def client_worker(client_id: int):
            client = self._create_websocket_client("localhost", 19006)
            time.sleep(0.1)

            message = f"Client {client_id} message"
            client.send(self._encode_message(message))
            time.sleep(0.1)

            response = client.recv(1024)
            decoded = self._decode_message(response)
            assert decoded == f"Echo: {message}"

            client.close()

        # 5개의 클라이언트 스레드 생성
        threads = []
        for i in range(5):
            thread = threading.Thread(target=client_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # 모든 스레드 종료 대기
        for thread in threads:
            thread.join(timeout=5.0)

        time.sleep(0.5)

        # 서버 중지
        server.stop()

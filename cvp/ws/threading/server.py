# -*- coding: utf-8 -*-

import socket
import struct
import threading
from base64 import b64encode
from hashlib import sha1
from typing import Callable, Dict, Optional, Set

from cvp.logging.loggers import logger


class WebSocketServer:
    """순수 Threading 모델 기반 WebSocket 서버"""

    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        message_handler: Optional[Callable[[socket.socket, str], None]] = None,
    ):
        """
        Args:
            host: 서버 호스트 주소
            port: 서버 포트 번호
            message_handler: 메시지 처리 핸들러 함수
        """
        self._host = host
        self._port = port
        self._message_handler = message_handler or self._default_message_handler
        self._clients: Set[socket.socket] = set()
        self._clients_lock = threading.Lock()
        self._server_socket: Optional[socket.socket] = None
        self._running = False
        self._accept_thread: Optional[threading.Thread] = None

    def _default_message_handler(
        self, client_socket: socket.socket, message: str
    ) -> None:
        """
        기본 메시지 핸들러 - 에코 서버

        Args:
            client_socket: 클라이언트 소켓
            message: 수신된 메시지
        """
        logger.info(f"수신된 메시지: {message}")
        # 에코: 받은 메시지를 그대로 돌려보냄
        self._send_message(client_socket, f"Echo: {message}")

    def _perform_handshake(self, client_socket: socket.socket) -> bool:
        """
        WebSocket 핸드셰이크 수행

        Args:
            client_socket: 클라이언트 소켓

        Returns:
            핸드셰이크 성공 여부
        """
        try:
            # HTTP 요청 헤더 읽기
            request = client_socket.recv(1024).decode("utf-8")
            headers = self._parse_headers(request)

            # Sec-WebSocket-Key 추출
            key = headers.get("Sec-WebSocket-Key")
            if not key:
                logger.error("Sec-WebSocket-Key가 없습니다")
                return False

            # Accept 키 생성
            accept_key = b64encode(
                sha1((key + self.MAGIC_STRING).encode()).digest()
            ).decode()

            # 핸드셰이크 응답 전송
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n"
                "\r\n"
            )
            client_socket.send(response.encode())
            return True

        except Exception as e:
            logger.error(f"핸드셰이크 실패: {e}")
            return False

    def _parse_headers(self, request: str) -> Dict[str, str]:
        """HTTP 헤더 파싱"""
        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return headers

    def _decode_frame(self, data: bytes) -> Optional[str]:
        """
        WebSocket 프레임 디코딩

        Args:
            data: 인코딩된 프레임 데이터

        Returns:
            디코딩된 메시지 또는 None
        """
        if len(data) < 2:
            return None

        # 첫 번째 바이트: FIN, RSV, opcode
        # 두 번째 바이트: MASK, payload length
        second_byte = data[1]
        mask = second_byte & 0x80
        payload_length = second_byte & 0x7F

        # Payload length 처리
        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            mask_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            mask_start = 10
        else:
            mask_start = 2

        if not mask:
            return None

        # 마스킹 키
        masking_key = data[mask_start : mask_start + 4]
        payload_start = mask_start + 4

        # 페이로드 디코딩
        payload = bytearray(data[payload_start : payload_start + payload_length])
        for i in range(len(payload)):
            payload[i] ^= masking_key[i % 4]

        return payload.decode("utf-8")

    def _encode_frame(self, message: str) -> bytes:
        """
        WebSocket 프레임 인코딩

        Args:
            message: 전송할 메시지

        Returns:
            인코딩된 프레임 데이터
        """
        payload = message.encode("utf-8")
        payload_length = len(payload)

        # 첫 번째 바이트: FIN=1, opcode=1 (text)
        frame = bytearray([0x81])

        # Payload length
        if payload_length <= 125:
            frame.append(payload_length)
        elif payload_length <= 65535:
            frame.append(126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(127)
            frame.extend(struct.pack(">Q", payload_length))

        # Payload
        frame.extend(payload)
        return bytes(frame)

    def _send_message(self, client_socket: socket.socket, message: str) -> None:
        """메시지 전송"""
        try:
            frame = self._encode_frame(message)
            client_socket.send(frame)
        except Exception as e:
            logger.error(f"메시지 전송 실패: {e}")

    def _handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        클라이언트 연결 처리

        Args:
            client_socket: 클라이언트 소켓
            address: 클라이언트 주소
        """
        client_info = f"{address[0]}:{address[1]}"

        try:
            # WebSocket 핸드셰이크
            if not self._perform_handshake(client_socket):
                logger.error(f"핸드셰이크 실패: {client_info}")
                return

            # 클라이언트 등록
            with self._clients_lock:
                self._clients.add(client_socket)
            logger.info(f"클라이언트 연결: {client_info} (총 {len(self._clients)}명)")

            # 메시지 수신 루프
            while self._running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    message = self._decode_frame(data)
                    if message:
                        # 메시지 핸들러 호출
                        self._message_handler(client_socket, message)

                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"메시지 처리 중 오류 ({client_info}): {e}")
                    break

        except Exception as e:
            logger.error(f"클라이언트 처리 중 오류 ({client_info}): {e}")
        finally:
            # 클라이언트 제거
            with self._clients_lock:
                self._clients.discard(client_socket)
            try:
                client_socket.close()
            except Exception:
                pass
            logger.info(
                f"클라이언트 제거: {client_info} (남은 연결: {len(self._clients)}명)"
            )

    def _accept_connections(self) -> None:
        """클라이언트 연결 수락 루프"""
        while self._running:
            try:
                if not self._server_socket:
                    break
                client_socket, address = self._server_socket.accept()
                # 각 클라이언트를 별도 스레드에서 처리
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True,
                )
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    logger.error(f"연결 수락 중 오류: {e}")

    def start(self) -> None:
        """서버 시작"""
        if self._running:
            logger.warning("서버가 이미 실행 중입니다")
            return

        self._running = True

        # 서버 소켓 생성
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(1.0)  # 1초 타임아웃으로 종료 가능하도록
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(5)

        logger.info(f"WebSocket 서버 시작: ws://{self._host}:{self._port}")

        # 별도 스레드에서 연결 수락
        self._accept_thread = threading.Thread(
            target=self._accept_connections, name="WebSocketAcceptThread", daemon=True
        )
        self._accept_thread.start()

    def stop(self) -> None:
        """서버 중지"""
        if not self._running:
            logger.warning("서버가 실행 중이 아닙니다")
            return

        self._running = False

        # 모든 클라이언트 연결 종료
        with self._clients_lock:
            if self._clients:
                logger.info(f"{len(self._clients)}개의 클라이언트 연결 종료 중...")
                for client in list(self._clients):
                    try:
                        client.close()
                    except Exception:
                        pass
                self._clients.clear()

        # 서버 소켓 종료
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass

        # 스레드 종료 대기
        if self._accept_thread:
            self._accept_thread.join(timeout=5.0)
            if self._accept_thread.is_alive():
                logger.warning("서버 스레드가 정상적으로 종료되지 않았습니다")

        logger.info("WebSocket 서버 중지")

    def broadcast(self, message: str) -> None:
        """
        모든 연결된 클라이언트에게 메시지 브로드캐스트

        Args:
            message: 전송할 메시지
        """
        with self._clients_lock:
            if not self._clients:
                logger.debug("연결된 클라이언트가 없습니다")
                return

            logger.debug(f"{len(self._clients)}명에게 브로드캐스트: {message}")

            disconnected = set()
            for client in self._clients:
                try:
                    self._send_message(client, message)
                except Exception as e:
                    logger.error(f"브로드캐스트 중 오류: {e}")
                    disconnected.add(client)

            # 연결이 끊긴 클라이언트 제거
            self._clients -= disconnected

    @property
    def is_running(self) -> bool:
        """서버 실행 상태 확인"""
        return self._running

    @property
    def client_count(self) -> int:
        """연결된 클라이언트 수"""
        with self._clients_lock:
            return len(self._clients)

# -*- coding: utf-8 -*-

import socket
import struct
import threading
import time
from base64 import b64encode
from os import urandom
from typing import Callable, Optional
from urllib.parse import urlparse

from cvp.logging.loggers import logger


class WebSocketClient:
    """순수 Threading 모델 기반 WebSocket 클라이언트"""

    def __init__(
        self,
        uri: str,
        reconnect_interval: float = 5.0,
        message_handler: Optional[Callable[[str], None]] = None,
    ):
        """
        Args:
            uri: WebSocket 서버 URI (예: ws://localhost:8765)
            reconnect_interval: 재연결 시도 간격(초)
            message_handler: 메시지 수신 핸들러 함수
        """
        self._uri = uri
        self._reconnect_interval = reconnect_interval
        self._message_handler = message_handler or self._default_message_handler
        self._socket: Optional[socket.socket] = None
        self._running = False
        self._connected = False
        self._receive_thread: Optional[threading.Thread] = None
        self._reconnect_thread: Optional[threading.Thread] = None

        # URI 파싱
        parsed = urlparse(uri)
        self._host = parsed.hostname or "localhost"
        self._port = parsed.port or 8765
        self._path = parsed.path or "/"

    def _default_message_handler(self, message: str) -> None:
        """
        기본 메시지 핸들러

        Args:
            message: 수신된 메시지
        """
        logger.info(f"수신된 메시지: {message}")

    def _perform_handshake(self) -> bool:
        """
        WebSocket 핸드셰이크 수행

        Returns:
            핸드셰이크 성공 여부
        """
        if not self._socket:
            return False

        try:
            # Sec-WebSocket-Key 생성
            key = b64encode(urandom(16)).decode()

            # HTTP 업그레이드 요청
            request = (
                f"GET {self._path} HTTP/1.1\r\n"
                f"Host: {self._host}:{self._port}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n"
                "\r\n"
            )
            self._socket.send(request.encode())

            # 응답 읽기
            response = self._socket.recv(1024).decode("utf-8")

            # 101 Switching Protocols 확인
            if "101 Switching Protocols" not in response:
                logger.error("핸드셰이크 실패: 101 응답이 아님")
                return False

            return True

        except Exception as e:
            logger.error(f"핸드셰이크 실패: {e}")
            return False

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
        payload_length = second_byte & 0x7F

        # Payload length 처리
        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            payload_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            payload_start = 10
        else:
            payload_start = 2

        # 서버에서 클라이언트로 전송하는 데이터는 마스킹되지 않음
        payload = data[payload_start : payload_start + payload_length]
        return payload.decode("utf-8")

    def _encode_frame(self, message: str) -> bytes:
        """
        WebSocket 프레임 인코딩 (마스킹 포함)

        Args:
            message: 전송할 메시지

        Returns:
            인코딩된 프레임 데이터
        """
        payload = message.encode("utf-8")
        payload_length = len(payload)

        # 첫 번째 바이트: FIN=1, opcode=1 (text)
        frame = bytearray([0x81])

        # 두 번째 바이트: MASK=1, payload length
        if payload_length <= 125:
            frame.append(0x80 | payload_length)
        elif payload_length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", payload_length))

        # 마스킹 키 생성
        masking_key = urandom(4)
        frame.extend(masking_key)

        # 페이로드 마스킹
        masked_payload = bytearray(payload)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    def connect(self) -> bool:
        """
        WebSocket 서버에 연결

        Returns:
            연결 성공 여부
        """
        try:
            # 소켓 생성
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(5.0)
            self._socket.connect((self._host, self._port))

            # 핸드셰이크
            if not self._perform_handshake():
                logger.error("핸드셰이크 실패")
                self.disconnect()
                return False

            self._connected = True
            self._socket.settimeout(1.0)  # 수신 타임아웃 설정
            logger.info(f"WebSocket 연결 성공: {self._uri}")
            return True

        except Exception as e:
            logger.error(f"WebSocket 연결 실패: {e}")
            self.disconnect()
            return False

    def disconnect(self) -> None:
        """WebSocket 연결 종료"""
        self._connected = False
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None
            logger.info("WebSocket 연결 종료")

    def send(self, message: str) -> bool:
        """
        메시지 전송

        Args:
            message: 전송할 메시지

        Returns:
            전송 성공 여부
        """
        if not self._connected or not self._socket:
            logger.error("WebSocket이 연결되지 않았습니다")
            return False

        try:
            frame = self._encode_frame(message)
            self._socket.send(frame)
            logger.debug(f"메시지 전송: {message}")
            return True
        except Exception as e:
            logger.error(f"메시지 전송 실패: {e}")
            self._connected = False
            return False

    def _receive_loop(self) -> None:
        """메시지 수신 루프 (별도 스레드에서 실행)"""
        while self._running and self._connected:
            if not self._socket:
                break
            try:
                data = self._socket.recv(4096)
                if not data:
                    logger.warning("WebSocket 연결이 닫혔습니다")
                    self._connected = False
                    break

                message = self._decode_frame(data)
                if message:
                    # 메시지 핸들러 호출
                    try:
                        self._message_handler(message)
                    except Exception as e:
                        logger.error(f"메시지 핸들러 오류: {e}")

            except socket.timeout:
                continue
            except Exception as e:
                if self._running and self._connected:
                    logger.error(f"메시지 수신 중 오류: {e}")
                self._connected = False
                break

    def _reconnect_loop(self) -> None:
        """자동 재연결 루프 (별도 스레드에서 실행)"""
        while self._running:
            if not self._connected:
                logger.info(f"{self._reconnect_interval}초 후 재연결 시도...")
                time.sleep(self._reconnect_interval)

                if not self._running:
                    break

                if self.connect():
                    # 재연결 성공 시 수신 스레드 재시작
                    self._receive_thread = threading.Thread(
                        target=self._receive_loop,
                        name="WebSocketReceiveThread",
                        daemon=True,
                    )
                    self._receive_thread.start()
            else:
                time.sleep(1.0)

    def start(self) -> None:
        """WebSocket 클라이언트 시작 (자동 재연결 포함)"""
        if self._running:
            logger.warning("클라이언트가 이미 실행 중입니다")
            return

        self._running = True

        # 초기 연결
        if self.connect():
            # 수신 스레드 시작
            self._receive_thread = threading.Thread(
                target=self._receive_loop,
                name="WebSocketReceiveThread",
                daemon=True,
            )
            self._receive_thread.start()

        # 재연결 스레드 시작
        self._reconnect_thread = threading.Thread(
            target=self._reconnect_loop,
            name="WebSocketReconnectThread",
            daemon=True,
        )
        self._reconnect_thread.start()

        logger.info("WebSocket 클라이언트 시작")

    def stop(self) -> None:
        """WebSocket 클라이언트 중지"""
        if not self._running:
            logger.warning("클라이언트가 실행 중이 아닙니다")
            return

        self._running = False
        self.disconnect()

        # 스레드 종료 대기
        if self._receive_thread:
            self._receive_thread.join(timeout=5.0)
        if self._reconnect_thread:
            self._reconnect_thread.join(timeout=5.0)

        logger.info("WebSocket 클라이언트 중지")

    @property
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        return self._connected

    @property
    def is_running(self) -> bool:
        """실행 상태 확인"""
        return self._running

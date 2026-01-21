# -*- coding: utf-8 -*-

import socket
import struct
import threading
import time
from base64 import b64encode
from os import urandom
from typing import Callable, Optional
from urllib.parse import urlparse

from cvp.logging.loggers import ws_logger as logger
from cvp.variables import AGENT_WS_PORT, LOCALHOST, ROOT_PATH


class WebSocketClient:
    def __init__(
        self,
        uri: str,
        reconnect_interval: float = 5.0,
        message_handler: Optional[Callable[[str], None]] = None,
    ):
        self._uri = uri
        self._reconnect_interval = reconnect_interval
        self._message_handler = message_handler or self._default_message_handler
        self._socket: Optional[socket.socket] = None
        self._running = False
        self._connected = False
        self._receive_thread: Optional[threading.Thread] = None
        self._reconnect_thread: Optional[threading.Thread] = None

        # Parse URI
        parsed = urlparse(uri)
        self._host = parsed.hostname or LOCALHOST
        self._port = parsed.port or AGENT_WS_PORT
        self._path = parsed.path or ROOT_PATH

    def _default_message_handler(self, message: str) -> None:
        """
        Default message handler

        Args:
            message: Received message
        """
        logger.info(f"Received message: {message}")

    def _perform_handshake(self) -> bool:
        """
        Perform WebSocket handshake

        Returns:
            Whether handshake succeeded
        """
        if not self._socket:
            return False

        try:
            # Generate Sec-WebSocket-Key
            key = b64encode(urandom(16)).decode()

            # HTTP upgrade request
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

            # Read response
            response = self._socket.recv(1024).decode("utf-8")

            # Verify 101 Switching Protocols
            if "101 Switching Protocols" not in response:
                logger.error("Handshake failed: Not a 101 response")
                return False

            return True

        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            return False

    def _decode_frame(self, data: bytes) -> Optional[str]:
        """
        Decode WebSocket frame

        Args:
            data: Encoded frame data

        Returns:
            Decoded message or None
        """
        if len(data) < 2:
            return None

        # First byte: FIN, RSV, opcode
        # Second byte: MASK, payload length
        second_byte = data[1]
        payload_length = second_byte & 0x7F

        # Handle payload length
        if payload_length == 126:
            payload_length = struct.unpack(">H", data[2:4])[0]
            payload_start = 4
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", data[2:10])[0]
            payload_start = 10
        else:
            payload_start = 2

        # Data sent from server to client is not masked
        payload = data[payload_start : payload_start + payload_length]
        return payload.decode("utf-8")

    def _encode_frame(self, message: str) -> bytes:
        """
        Encode WebSocket frame (with masking)

        Args:
            message: Message to send

        Returns:
            Encoded frame data
        """
        payload = message.encode("utf-8")
        payload_length = len(payload)

        # First byte: FIN=1, opcode=1 (text)
        frame = bytearray([0x81])

        # Second byte: MASK=1, payload length
        if payload_length <= 125:
            frame.append(0x80 | payload_length)
        elif payload_length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", payload_length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", payload_length))

        # Generate masking key
        masking_key = urandom(4)
        frame.extend(masking_key)

        # Mask payload
        masked_payload = bytearray(payload)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    def connect(self) -> bool:
        """
        Connect to WebSocket server

        Returns:
            Whether connection succeeded
        """
        try:
            # Create socket
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(5.0)
            self._socket.connect((self._host, self._port))

            # Handshake
            if not self._perform_handshake():
                logger.error("Handshake failed")
                self.disconnect()
                return False

            self._connected = True
            self._socket.settimeout(1.0)  # Set receive timeout
            logger.info(f"WebSocket connected: {self._uri}")
            return True

        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            self.disconnect()
            return False

    def disconnect(self) -> None:
        """Disconnect WebSocket connection"""
        self._connected = False
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None
            logger.info("WebSocket disconnected")

    def send(self, message: str) -> bool:
        """
        Send message

        Args:
            message: Message to send

        Returns:
            Whether sending succeeded
        """
        if not self._connected or not self._socket:
            logger.error("WebSocket is not connected")
            return False

        try:
            frame = self._encode_frame(message)
            self._socket.send(frame)
            logger.debug(f"Message sent: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self._connected = False
            return False

    def _receive_loop(self) -> None:
        """Message receive loop (runs in separate thread)"""
        while self._running and self._connected:
            if not self._socket:
                break
            try:
                data = self._socket.recv(4096)
                if not data:
                    logger.warning("WebSocket connection closed")
                    self._connected = False
                    break

                message = self._decode_frame(data)
                if message:
                    # Call message handler
                    try:
                        self._message_handler(message)
                    except Exception as e:
                        logger.error(f"Message handler error: {e}")

            except socket.timeout:
                continue
            except Exception as e:
                if self._running and self._connected:
                    logger.error(f"Error receiving message: {e}")
                self._connected = False
                break

    def _reconnect_loop(self) -> None:
        """Auto reconnect loop (runs in separate thread)"""
        while self._running:
            if not self._connected:
                logger.info(f"Reconnecting in {self._reconnect_interval} seconds...")
                time.sleep(self._reconnect_interval)

                if not self._running:
                    break

                if self.connect():
                    # Restart receive thread on successful reconnection
                    self._receive_thread = threading.Thread(
                        target=self._receive_loop,
                        name="WebSocketReceiveThread",
                        daemon=True,
                    )
                    self._receive_thread.start()
            else:
                time.sleep(1.0)

    def start(self) -> None:
        """Start WebSocket client (with auto reconnection)"""
        if self._running:
            logger.warning("Client is already running")
            return

        self._running = True

        # Initial connection
        if self.connect():
            # Start receive thread
            self._receive_thread = threading.Thread(
                target=self._receive_loop,
                name="WebSocketReceiveThread",
                daemon=True,
            )
            self._receive_thread.start()

        # Start reconnect thread
        self._reconnect_thread = threading.Thread(
            target=self._reconnect_loop,
            name="WebSocketReconnectThread",
            daemon=True,
        )
        self._reconnect_thread.start()

        logger.info("WebSocket client started")

    def stop(self) -> None:
        """Stop WebSocket client"""
        if not self._running:
            logger.warning("Client is not running")
            return

        self._running = False
        self.disconnect()

        # Wait for threads to finish
        if self._receive_thread:
            self._receive_thread.join(timeout=5.0)
        if self._reconnect_thread:
            self._reconnect_thread.join(timeout=5.0)

        logger.info("WebSocket client stopped")

    @property
    def is_connected(self) -> bool:
        """Check connection status"""
        return self._connected

    @property
    def is_running(self) -> bool:
        """Check running status"""
        return self._running

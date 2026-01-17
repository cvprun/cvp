# -*- coding: utf-8 -*-

import socket
import struct
import threading
from base64 import b64encode
from hashlib import sha1
from typing import Callable, Dict, Optional, Set

from cvp.logging.loggers import ws_logger as logger


class WebSocketServer:
    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        message_handler: Optional[Callable[[socket.socket, str], None]] = None,
    ):
        """
        Args:
            host: Server host address
            port: Server port number
            message_handler: Message processing handler function
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
        Default message handler - echo server

        Args:
            client_socket: Client socket
            message: Received message
        """
        logger.info(f"Received message: {message}")
        # Echo: send back the received message
        self._send_message(client_socket, f"Echo: {message}")

    def _perform_handshake(self, client_socket: socket.socket) -> bool:
        """
        Perform WebSocket handshake

        Args:
            client_socket: Client socket

        Returns:
            Whether handshake succeeded
        """
        try:
            # Read HTTP request headers
            request = client_socket.recv(1024).decode("utf-8")
            headers = self._parse_headers(request)

            # Extract Sec-WebSocket-Key
            key = headers.get("Sec-WebSocket-Key")
            if not key:
                logger.error("Sec-WebSocket-Key not found")
                return False

            # Generate accept key
            accept_key = b64encode(
                sha1((key + self.MAGIC_STRING).encode()).digest()
            ).decode()

            # Send handshake response
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
            logger.error(f"Handshake failed: {e}")
            return False

    def _parse_headers(self, request: str) -> Dict[str, str]:
        """Parse HTTP headers"""
        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return headers

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
        mask = second_byte & 0x80
        payload_length = second_byte & 0x7F

        # Handle payload length
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

        # Masking key
        masking_key = data[mask_start : mask_start + 4]
        payload_start = mask_start + 4

        # Decode payload
        payload = bytearray(data[payload_start : payload_start + payload_length])
        for i in range(len(payload)):
            payload[i] ^= masking_key[i % 4]

        return payload.decode("utf-8")

    def _encode_frame(self, message: str) -> bytes:
        """
        Encode WebSocket frame

        Args:
            message: Message to send

        Returns:
            Encoded frame data
        """
        payload = message.encode("utf-8")
        payload_length = len(payload)

        # First byte: FIN=1, opcode=1 (text)
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
        """Send message"""
        try:
            frame = self._encode_frame(message)
            client_socket.send(frame)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def _handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Handle client connection

        Args:
            client_socket: Client socket
            address: Client address
        """
        client_info = f"{address[0]}:{address[1]}"

        try:
            # WebSocket handshake
            if not self._perform_handshake(client_socket):
                logger.error(f"Handshake failed: {client_info}")
                return

            # Register client
            with self._clients_lock:
                self._clients.add(client_socket)
            logger.info(f"Client connected: {client_info} (total {len(self._clients)})")

            # Message receive loop
            while self._running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    message = self._decode_frame(data)
                    if message:
                        # Call message handler
                        self._message_handler(client_socket, message)

                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Error processing message ({client_info}): {e}")
                    break

        except Exception as e:
            logger.error(f"Error handling client ({client_info}): {e}")
        finally:
            # Remove client
            with self._clients_lock:
                self._clients.discard(client_socket)
            try:
                client_socket.close()
            except Exception:
                pass
            logger.info(
                f"Client removed: {client_info} (remaining {len(self._clients)})"
            )

    def _accept_connections(self) -> None:
        """Client connection accept loop"""
        while self._running:
            try:
                if not self._server_socket:
                    break
                client_socket, address = self._server_socket.accept()
                # Handle each client in separate thread
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
                    logger.error(f"Error accepting connection: {e}")

    def start(self) -> None:
        """Start server"""
        if self._running:
            logger.warning("Server is already running")
            return

        self._running = True

        # Create server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(1.0)  # 1 second timeout to allow shutdown
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(5)

        logger.info(f"WebSocket server started: ws://{self._host}:{self._port}")

        # Accept connections in separate thread
        self._accept_thread = threading.Thread(
            target=self._accept_connections, name="WebSocketAcceptThread", daemon=True
        )
        self._accept_thread.start()

    def stop(self) -> None:
        """Stop server"""
        if not self._running:
            logger.warning("Server is not running")
            return

        self._running = False

        # Close all client connections
        with self._clients_lock:
            if self._clients:
                logger.info(f"Closing {len(self._clients)} client connection(s)...")
                for client in list(self._clients):
                    try:
                        client.close()
                    except Exception:
                        pass
                self._clients.clear()

        # Close server socket
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass

        # Wait for thread to finish
        if self._accept_thread:
            self._accept_thread.join(timeout=5.0)
            if self._accept_thread.is_alive():
                logger.warning("Server thread did not terminate properly")

        logger.info("WebSocket server stopped")

    def broadcast(self, message: str) -> None:
        """
        Broadcast message to all connected clients

        Args:
            message: Message to send
        """
        with self._clients_lock:
            if not self._clients:
                logger.debug("No connected clients")
                return

            logger.debug(f"Broadcasting to {len(self._clients)} client(s): {message}")

            disconnected = set()
            for client in self._clients:
                try:
                    self._send_message(client, message)
                except Exception as e:
                    logger.error(f"Error during broadcast: {e}")
                    disconnected.add(client)

            # Remove disconnected clients
            self._clients -= disconnected

    @property
    def is_running(self) -> bool:
        """Check server running status"""
        return self._running

    @property
    def client_count(self) -> int:
        """Number of connected clients"""
        with self._clients_lock:
            return len(self._clients)

# -*- coding: utf-8 -*-

import socket
import struct
import threading
from base64 import b64encode
from hashlib import sha1
from typing import Callable, Dict, Final, Optional, Set, Tuple, Union

from cvp.logging.loggers import ws_logger as logger
from cvp.variables import EPHEMERAL_PORT, LOCALHOST
from cvp.ws.handlers.message_handler import MessageHandler

OPCODE_TEXT: Final[int] = 0x01
OPCODE_BINARY: Final[int] = 0x02
OPCODE_CLOSE: Final[int] = 0x08
OPCODE_PING: Final[int] = 0x09
OPCODE_PONG: Final[int] = 0x0A

MAGIC_STRING: Final[str] = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

TextMessageHandler = Callable[[socket.socket, str], Optional[str]]
BinaryMessageHandler = Callable[[socket.socket, bytes], Optional[bytes]]


class WebSocketServer:
    def __init__(
        self,
        host: str = LOCALHOST,
        port: int = EPHEMERAL_PORT,
        message_handler: Optional[TextMessageHandler] = None,
        binary_handler: Optional[BinaryMessageHandler] = None,
        handler: Optional[MessageHandler] = None,
    ):
        self._host = host
        self._requested_port = port
        self._bound_port: Optional[int] = None
        self._message_handler = message_handler or self._default_message_handler
        self._binary_handler = binary_handler
        self._handler = handler
        self._clients: Set[socket.socket] = set()
        self._clients_lock = threading.Lock()
        self._server_socket: Optional[socket.socket] = None
        self._running = False
        self._accept_thread: Optional[threading.Thread] = None

    @staticmethod
    def _default_message_handler(
        client_socket: socket.socket, message: str
    ) -> Optional[str]:
        logger.info(f"Received message: {message}")
        # Echo: send back the received message
        return f"Echo: {message}"

    def _perform_handshake(self, client_socket: socket.socket) -> bool:
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
                sha1((key + MAGIC_STRING).encode()).digest()
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
        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return headers

    def _decode_frame(
        self, data: bytes
    ) -> Tuple[Optional[int], Optional[Union[str, bytes]]]:
        """Decode WebSocket frame.

        Returns:
            Tuple of (opcode, payload). opcode is None if decoding fails.
            For text frames, payload is str. For binary frames, payload is bytes.
        """
        if len(data) < 2:
            return None, None

        # First byte: FIN, RSV, opcode
        first_byte = data[0]
        opcode = first_byte & 0x0F

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
            return opcode, None

        # Masking key
        masking_key = data[mask_start : mask_start + 4]
        payload_start = mask_start + 4

        # Decode payload
        payload = bytearray(data[payload_start : payload_start + payload_length])
        for i in range(len(payload)):
            payload[i] ^= masking_key[i % 4]

        # Return based on opcode
        if opcode == OPCODE_TEXT:
            return opcode, payload.decode("utf-8")
        elif opcode == OPCODE_BINARY:
            return opcode, bytes(payload)
        else:
            return opcode, bytes(payload)

    def _encode_frame(self, message: str) -> bytes:
        """Encode text message as WebSocket frame."""
        payload = message.encode("utf-8")
        return self._encode_frame_with_opcode(OPCODE_TEXT, payload)

    def _encode_binary_frame(self, data: bytes) -> bytes:
        """Encode binary data as WebSocket frame."""
        return self._encode_frame_with_opcode(OPCODE_BINARY, data)

    def _encode_frame_with_opcode(self, opcode: int, payload: bytes) -> bytes:
        """Encode WebSocket frame with specified opcode.

        Args:
            opcode: WebSocket opcode (OPCODE_TEXT or OPCODE_BINARY).
            payload: Payload bytes.

        Returns:
            Encoded WebSocket frame.
        """
        payload_length = len(payload)

        # First byte: FIN=1, opcode
        frame = bytearray([0x80 | opcode])

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
        """Send text message to client."""
        try:
            frame = self._encode_frame(message)
            client_socket.send(frame)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def _send_binary(self, client_socket: socket.socket, data: bytes) -> None:
        """Send binary data to client."""
        try:
            frame = self._encode_binary_frame(data)
            client_socket.send(frame)
        except Exception as e:
            logger.error(f"Failed to send binary data: {e}")

    def _handle_client(self, client_socket: socket.socket, address: tuple) -> None:
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

            # Notify handler of connection
            if self._handler:
                self._handler.on_connect()

            # Message receive loop
            while self._running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    opcode, payload = self._decode_frame(data)
                    if opcode is None or payload is None:
                        continue

                    # Handle based on opcode
                    if opcode == OPCODE_TEXT and isinstance(payload, str):
                        # Text message
                        text_response = self._message_handler(client_socket, payload)
                        if text_response:
                            self._send_message(client_socket, text_response)
                    elif opcode == OPCODE_BINARY and isinstance(payload, bytes):
                        # Binary message - use handler or binary_handler
                        if self._handler:
                            binary_response = self._handler.on_message(payload)
                            if binary_response:
                                self._send_binary(client_socket, binary_response)
                        elif self._binary_handler:
                            binary_response = self._binary_handler(
                                client_socket, payload
                            )
                            if binary_response:
                                self._send_binary(client_socket, binary_response)
                    elif opcode == OPCODE_CLOSE:
                        logger.debug(f"Close frame received: {client_info}")
                        break
                    elif opcode == OPCODE_PING and isinstance(payload, bytes):
                        # Send pong response
                        pong_frame = self._encode_frame_with_opcode(
                            OPCODE_PONG, payload
                        )
                        client_socket.send(pong_frame)

                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Error processing message ({client_info}): {e}")
                    break

        except Exception as e:
            logger.error(f"Error handling client ({client_info}): {e}")
        finally:
            # Notify handler of disconnection
            if self._handler:
                self._handler.on_disconnect()

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
        if self._running:
            logger.warning("Server is already running")
            return

        self._running = True

        # Create server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(1.0)  # 1 second timeout to allow shutdown

        # Use port 0 for ephemeral port assignment when requested port is -1
        bind_port = 0 if self._requested_port == -1 else self._requested_port
        self._server_socket.bind((self._host, bind_port))
        self._server_socket.listen(5)

        # Store the actual bound port (important for random port assignment)
        self._bound_port = self._server_socket.getsockname()[1]

        logger.info(f"WebSocket server started: ws://{self._host}:{self._bound_port}")

        # Accept connections in separate thread
        self._accept_thread = threading.Thread(
            target=self._accept_connections, name="WebSocketAcceptThread", daemon=True
        )
        self._accept_thread.start()

    def stop(self) -> None:
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

        self._bound_port = None

        # Wait for thread to finish
        if self._accept_thread:
            self._accept_thread.join(timeout=5.0)
            if self._accept_thread.is_alive():
                logger.warning("Server thread did not terminate properly")

        logger.info("WebSocket server stopped")

    def broadcast(self, message: str) -> None:
        """Broadcast text message to all connected clients."""
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

    def broadcast_binary(self, data: bytes) -> None:
        """Broadcast binary data to all connected clients."""
        with self._clients_lock:
            if not self._clients:
                logger.debug("No connected clients")
                return

            logger.debug(f"Broadcasting binary to {len(self._clients)} client(s)")

            disconnected = set()
            for client in self._clients:
                try:
                    self._send_binary(client, data)
                except Exception as e:
                    logger.error(f"Error during binary broadcast: {e}")
                    disconnected.add(client)

            # Remove disconnected clients
            self._clients -= disconnected

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def client_count(self) -> int:
        with self._clients_lock:
            return len(self._clients)

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        """Return the actual bound port. Returns -1 if not yet bound."""
        if self._bound_port is not None:
            return self._bound_port
        return self._requested_port

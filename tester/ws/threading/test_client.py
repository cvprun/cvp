# -*- coding: utf-8 -*-

import socket
import struct
import threading
import time
from base64 import b64encode
from hashlib import sha1

from cvp.ws.threading.client import WebSocketClient


class SimpleWebSocketServer:
    """Simple WebSocket server for testing"""

    MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None

    def _perform_handshake(self, client_socket: socket.socket) -> bool:
        """Perform WebSocket handshake"""
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
        """Decode WebSocket frame"""
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
        """Encode WebSocket frame"""
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
        """Handle client connection"""
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
                    # Echo response
                    response = self._encode_frame(f"Echo: {message}")
                    client_socket.send(response)
        except Exception:
            pass
        finally:
            client_socket.close()

    def _accept_loop(self):
        """Client connection accept loop"""
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
        """Start server"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1.0)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.thread = threading.Thread(target=self._accept_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join(timeout=2.0)


class TestWebSocketClient:
    """Tests for threading-based WebSocket client"""

    def test_client_connect_disconnect(self):
        """Test client connection and disconnection"""
        # Start test server
        server = SimpleWebSocketServer("localhost", 19101)
        server.start()
        time.sleep(0.5)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:19101")
            success = client.connect()

            assert success
            assert client.is_connected

            # Disconnect
            client.disconnect()

            assert not client.is_connected

        finally:
            server.stop()

    def test_client_send_receive(self):
        """Test client message send and receive"""
        # Start test server
        server = SimpleWebSocketServer("localhost", 19102)
        server.start()
        time.sleep(0.5)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:19102")
            client.connect()

            # Send message
            success = client.send("Hello Server")
            assert success

            time.sleep(0.1)

            # Disconnect
            client.disconnect()

        finally:
            server.stop()

    def test_client_message_handler(self):
        """Test client message handler"""
        received_messages = []

        def message_handler(message: str):
            received_messages.append(message)

        # Start test server
        server = SimpleWebSocketServer("localhost", 19103)
        server.start()
        time.sleep(0.5)

        try:
            # Create and start client
            client = WebSocketClient(
                "ws://localhost:19103", message_handler=message_handler
            )
            client.start()

            # Wait for connection
            time.sleep(0.5)
            assert client.is_connected

            # Send message
            client.send("Test message")

            # Wait for response
            time.sleep(0.5)

            assert len(received_messages) > 0
            assert "Echo: Test message" in received_messages

            # Stop client
            client.stop()

        finally:
            server.stop()

    def test_client_reconnect(self):
        """Test client reconnection"""
        # Start test server
        server = SimpleWebSocketServer("localhost", 19104)
        server.start()
        time.sleep(0.5)

        try:
            # Set short interval for fast reconnection
            client = WebSocketClient("ws://localhost:19104", reconnect_interval=0.5)
            client.start()

            # Wait for connection
            time.sleep(0.5)
            assert client.is_connected

            # Force disconnect
            if client._socket:
                client._socket.close()
                client._connected = False

            # Wait for reconnection
            time.sleep(1.5)

            # Verify reconnection
            assert client.is_connected

            # Stop client
            client.stop()

        finally:
            server.stop()

    def test_client_multiple_messages(self):
        """Test multiple message send and receive"""
        # Start test server
        server = SimpleWebSocketServer("localhost", 19105)
        server.start()
        time.sleep(0.5)

        try:
            # Create and connect client
            client = WebSocketClient("ws://localhost:19105")
            client.connect()

            # Send multiple messages
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                success = client.send(msg)
                assert success
                time.sleep(0.1)

            # Disconnect
            client.disconnect()

        finally:
            server.stop()

    def test_client_auto_start_with_reconnect(self):
        """Test auto start and reconnection"""
        # Start test server
        server = SimpleWebSocketServer("localhost", 19106)
        server.start()
        time.sleep(0.5)

        try:
            received_messages = []

            def message_handler(message: str):
                received_messages.append(message)

            # Auto start client
            client = WebSocketClient(
                "ws://localhost:19106",
                reconnect_interval=0.5,
                message_handler=message_handler,
            )
            client.start()

            # Wait for connection
            time.sleep(0.5)
            assert client.is_connected
            assert client.is_running

            # Send and receive message
            client.send("Auto test")
            time.sleep(0.5)

            assert len(received_messages) > 0

            # Stop client
            client.stop()

            assert not client.is_running

        finally:
            server.stop()

    def test_client_connection_failure(self):
        """Test connection failure"""
        # Try to connect without server
        client = WebSocketClient("ws://localhost:19999")
        success = client.connect()

        assert not success
        assert not client.is_connected

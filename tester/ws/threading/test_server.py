# -*- coding: utf-8 -*-

import socket
import threading
import time
from base64 import b64encode

from cvp.ws.threading.server import WebSocketServer


class TestWebSocketServer:
    """Tests for threading-based WebSocket server"""

    def _create_websocket_client(self, host: str, port: int) -> socket.socket:
        """Create WebSocket client socket and perform handshake"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # WebSocket handshake
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

        # Receive handshake response
        response = client.recv(1024)
        assert b"101 Switching Protocols" in response

        return client

    def _encode_message(self, message: str) -> bytes:
        """Encode WebSocket frame (client -> server)"""
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

        # Masking key
        masking_key = urandom(4)
        frame.extend(masking_key)

        # Mask payload
        masked_payload = bytearray(payload)
        for i in range(len(masked_payload)):
            masked_payload[i] ^= masking_key[i % 4]

        frame.extend(masked_payload)
        return bytes(frame)

    def _decode_message(self, data: bytes) -> str:
        """Decode WebSocket frame (server -> client)"""
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
        """Test server start and stop"""
        server = WebSocketServer(host="localhost", port=19001)

        # Start server
        server.start()
        time.sleep(0.5)

        assert server.is_running
        assert server.client_count == 0

        # Stop server
        server.stop()
        time.sleep(0.5)

        assert not server.is_running

    def test_server_client_connection(self):
        """Test client connection"""
        server = WebSocketServer(host="localhost", port=19002)

        # Start server
        server.start()
        time.sleep(0.5)

        # Connect client
        client = self._create_websocket_client("localhost", 19002)
        time.sleep(0.3)

        assert server.client_count == 1

        # Send and receive message (echo server)
        message = "Hello"
        client.send(self._encode_message(message))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        assert decoded == f"Echo: {message}"

        # Close client
        client.close()
        time.sleep(0.3)

        assert server.client_count == 0

        # Stop server
        server.stop()

    def test_server_custom_message_handler(self):
        """Test custom message handler"""
        received_messages = []

        def custom_handler(client_socket: socket.socket, message: str):
            received_messages.append(message)
            # Send response
            frame = bytearray([0x81])  # FIN=1, opcode=1
            payload = f"Received: {message}".encode("utf-8")
            frame.append(len(payload))
            frame.extend(payload)
            client_socket.send(bytes(frame))

        server = WebSocketServer(
            host="localhost", port=19003, message_handler=custom_handler
        )

        # Start server
        server.start()
        time.sleep(0.5)

        # Connect client and send message
        client = self._create_websocket_client("localhost", 19003)
        time.sleep(0.1)

        client.send(self._encode_message("Test message"))
        time.sleep(0.1)

        response = client.recv(1024)
        decoded = self._decode_message(response)
        assert decoded == "Received: Test message"
        assert "Test message" in received_messages

        # Close client
        client.close()

        # Stop server
        server.stop()

    def test_server_broadcast(self):
        """Test broadcast"""
        server = WebSocketServer(host="localhost", port=19004)

        # Start server
        server.start()
        time.sleep(0.5)

        # Connect multiple clients
        clients = []
        for _ in range(3):
            client = self._create_websocket_client("localhost", 19004)
            clients.append(client)

        time.sleep(0.3)
        assert server.client_count == 3

        # Broadcast
        server.broadcast("Broadcast message")
        time.sleep(0.1)

        # Verify all clients received the message
        for client in clients:
            response = client.recv(1024)
            decoded = self._decode_message(response)
            assert decoded == "Broadcast message"

        # Close clients
        for client in clients:
            client.close()

        time.sleep(0.3)

        # Stop server
        server.stop()

    def test_server_multiple_messages(self):
        """Test multiple message send and receive"""
        server = WebSocketServer(host="localhost", port=19005)

        # Start server
        server.start()
        time.sleep(0.5)

        # Connect client
        client = self._create_websocket_client("localhost", 19005)
        time.sleep(0.1)

        # Send multiple messages
        messages = ["Message 1", "Message 2", "Message 3"]
        for msg in messages:
            client.send(self._encode_message(msg))
            time.sleep(0.1)
            response = client.recv(1024)
            decoded = self._decode_message(response)
            assert decoded == f"Echo: {msg}"

        # Close client
        client.close()

        # Stop server
        server.stop()

    def test_server_concurrent_clients(self):
        """Test concurrent multiple clients"""
        server = WebSocketServer(host="localhost", port=19006)

        # Start server
        server.start()
        time.sleep(0.5)

        # Multiple clients send messages simultaneously
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

        # Create 5 client threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=client_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5.0)

        time.sleep(0.5)

        # Stop server
        server.stop()

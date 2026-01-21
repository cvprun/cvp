# -*- coding: utf-8 -*-

import socket
import struct
import threading
from typing import Optional, Set

from cvp.logging.loggers import modbus_logger as logger
from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.protocol import (
    COIL_ON,
    FC_READ_COILS,
    FC_READ_DISCRETE_INPUTS,
    FC_READ_HOLDING_REGISTERS,
    FC_READ_INPUT_REGISTERS,
    FC_WRITE_MULTIPLE_COILS,
    FC_WRITE_MULTIPLE_REGISTERS,
    FC_WRITE_SINGLE_COIL,
    FC_WRITE_SINGLE_REGISTER,
    MBAP_HEADER_SIZE,
    decode_mbap_header,
    encode_mbap_header,
)


class ModbusTcpServer:
    """Modbus TCP server with threading model."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 502,
        datastore: Optional[ModbusDataStore] = None,
        unit_id: int = 1,
    ):
        """Initialize the Modbus TCP server.

        Args:
            host: Server host address.
            port: Server port (default: 502).
            datastore: Data store for registers and coils (creates new if None).
            unit_id: Unit identifier (default: 1).
        """
        self._host = host
        self._port = port
        self._datastore = datastore or ModbusDataStore()
        self._unit_id = unit_id

        self._running = False
        self._server_socket: Optional[socket.socket] = None
        self._clients: Set[socket.socket] = set()
        self._clients_lock = threading.Lock()
        self._accept_thread: Optional[threading.Thread] = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def unit_id(self) -> int:
        return self._unit_id

    @property
    def datastore(self) -> ModbusDataStore:
        return self._datastore

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def client_count(self) -> int:
        with self._clients_lock:
            return len(self._clients)

    def start(self) -> None:
        """Start the Modbus TCP server."""
        if self._running:
            logger.warning("Server is already running")
            return

        self._running = True

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(1.0)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(5)

        logger.info(f"Modbus TCP server started on {self._host}:{self._port}")

        self._accept_thread = threading.Thread(
            target=self._accept_connections,
            name="ModbusAcceptThread",
            daemon=True,
        )
        self._accept_thread.start()

    def stop(self) -> None:
        """Stop the Modbus TCP server."""
        if not self._running:
            logger.warning("Server is not running")
            return

        self._running = False

        with self._clients_lock:
            if self._clients:
                logger.info(f"Closing {len(self._clients)} client connection(s)...")
                for client in list(self._clients):
                    try:
                        client.close()
                    except Exception:
                        pass
                self._clients.clear()

        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass
            self._server_socket = None

        if self._accept_thread:
            self._accept_thread.join(timeout=5.0)
            if self._accept_thread.is_alive():
                logger.warning("Server thread did not terminate properly")

        logger.info("Modbus TCP server stopped")

    def _accept_connections(self) -> None:
        """Accept incoming connections (runs in separate thread)."""
        while self._running:
            try:
                if not self._server_socket:
                    break
                client_socket, address = self._server_socket.accept()
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

    def _handle_client(
        self,
        client_socket: socket.socket,
        address: tuple,
    ) -> None:
        """Handle a connected client.

        Args:
            client_socket: Client socket.
            address: Client address tuple (host, port).
        """
        client_info = f"{address[0]}:{address[1]}"

        try:
            with self._clients_lock:
                self._clients.add(client_socket)
            logger.info(f"Client connected: {client_info} (total {self.client_count})")

            client_socket.settimeout(1.0)

            while self._running:
                try:
                    header_data = self._recv_exact(client_socket, MBAP_HEADER_SIZE)
                    if not header_data:
                        break

                    transaction_id, protocol_id, length, unit_id = decode_mbap_header(
                        header_data
                    )

                    if protocol_id != 0:
                        logger.warning(f"Invalid protocol ID: {protocol_id}")
                        continue

                    pdu_length = length - 1  # Length includes unit_id
                    if pdu_length <= 0:
                        continue

                    pdu_data = self._recv_exact(client_socket, pdu_length)
                    if not pdu_data:
                        break

                    response = self._process_request(transaction_id, unit_id, pdu_data)

                    if response:
                        client_socket.send(response)

                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Error processing request ({client_info}): {e}")
                    break

        except Exception as e:
            logger.error(f"Error handling client ({client_info}): {e}")
        finally:
            with self._clients_lock:
                self._clients.discard(client_socket)
            try:
                client_socket.close()
            except Exception:
                pass
            logger.info(f"Client disconnected: {client_info}")

    def _recv_exact(
        self,
        sock: socket.socket,
        length: int,
    ) -> Optional[bytes]:
        """Receive exactly the specified number of bytes.

        Args:
            sock: Socket to receive from.
            length: Number of bytes to receive.

        Returns:
            Received data or None if connection closed.
        """
        data = bytearray()
        while len(data) < length:
            try:
                chunk = sock.recv(length - len(data))
                if not chunk:
                    return None
                data.extend(chunk)
            except socket.timeout:
                if not self._running:
                    return None
                continue
        return bytes(data)

    def _process_request(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> Optional[bytes]:
        """Process a Modbus request and generate response.

        Args:
            transaction_id: Transaction identifier.
            unit_id: Unit identifier.
            pdu: Protocol Data Unit.

        Returns:
            Response frame or None.
        """
        if unit_id != self._unit_id and unit_id != 0:
            return None

        function_code = pdu[0]

        try:
            if function_code == FC_READ_COILS:
                return self._handle_read_coils(transaction_id, unit_id, pdu)
            elif function_code == FC_READ_DISCRETE_INPUTS:
                return self._handle_read_discrete_inputs(transaction_id, unit_id, pdu)
            elif function_code == FC_READ_HOLDING_REGISTERS:
                return self._handle_read_holding_registers(transaction_id, unit_id, pdu)
            elif function_code == FC_READ_INPUT_REGISTERS:
                return self._handle_read_input_registers(transaction_id, unit_id, pdu)
            elif function_code == FC_WRITE_SINGLE_COIL:
                return self._handle_write_single_coil(transaction_id, unit_id, pdu)
            elif function_code == FC_WRITE_SINGLE_REGISTER:
                return self._handle_write_single_register(transaction_id, unit_id, pdu)
            elif function_code == FC_WRITE_MULTIPLE_COILS:
                return self._handle_write_multiple_coils(transaction_id, unit_id, pdu)
            elif function_code == FC_WRITE_MULTIPLE_REGISTERS:
                return self._handle_write_multiple_registers(
                    transaction_id, unit_id, pdu
                )
            else:
                return self._build_error_response(
                    transaction_id, unit_id, function_code, 0x01
                )
        except Exception as e:
            logger.error(f"Error processing FC {function_code}: {e}")
            return self._build_error_response(
                transaction_id, unit_id, function_code, 0x04
            )

    def _handle_read_coils(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Read Coils (FC 0x01) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]

        coils = self._datastore.get_coils(address, count)

        byte_count = (count + 7) // 8
        coil_bytes = bytearray(byte_count)
        for i, value in enumerate(coils):
            if value:
                coil_bytes[i // 8] |= 1 << (i % 8)

        response_pdu = bytes([FC_READ_COILS, byte_count]) + bytes(coil_bytes)
        return self._build_response(transaction_id, unit_id, response_pdu)

    def _handle_read_discrete_inputs(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Read Discrete Inputs (FC 0x02) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]

        inputs = self._datastore.get_discrete_inputs(address, count)

        byte_count = (count + 7) // 8
        input_bytes = bytearray(byte_count)
        for i, value in enumerate(inputs):
            if value:
                input_bytes[i // 8] |= 1 << (i % 8)

        response_pdu = bytes([FC_READ_DISCRETE_INPUTS, byte_count]) + bytes(input_bytes)
        return self._build_response(transaction_id, unit_id, response_pdu)

    def _handle_read_holding_registers(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Read Holding Registers (FC 0x03) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]

        registers = self._datastore.get_holding_registers(address, count)

        byte_count = count * 2
        response_pdu = bytes([FC_READ_HOLDING_REGISTERS, byte_count])
        for reg in registers:
            response_pdu += struct.pack(">H", reg)

        return self._build_response(transaction_id, unit_id, response_pdu)

    def _handle_read_input_registers(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Read Input Registers (FC 0x04) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]

        registers = self._datastore.get_input_registers(address, count)

        byte_count = count * 2
        response_pdu = bytes([FC_READ_INPUT_REGISTERS, byte_count])
        for reg in registers:
            response_pdu += struct.pack(">H", reg)

        return self._build_response(transaction_id, unit_id, response_pdu)

    def _handle_write_single_coil(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Write Single Coil (FC 0x05) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        value = struct.unpack(">H", pdu[3:5])[0]

        coil_value = value == COIL_ON
        self._datastore.set_coil(address, coil_value)

        return self._build_response(transaction_id, unit_id, pdu)

    def _handle_write_single_register(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Write Single Register (FC 0x06) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        value = struct.unpack(">H", pdu[3:5])[0]

        self._datastore.set_holding_register(address, value)

        return self._build_response(transaction_id, unit_id, pdu)

    def _handle_write_multiple_coils(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Write Multiple Coils (FC 0x0F) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]
        byte_count = pdu[5]
        coil_data = pdu[6 : 6 + byte_count]

        values = []
        for i in range(count):
            byte_idx = i // 8
            bit_idx = i % 8
            if byte_idx < len(coil_data):
                values.append(bool(coil_data[byte_idx] & (1 << bit_idx)))
            else:
                values.append(False)

        self._datastore.set_coils(address, values)

        response_pdu = struct.pack(">BHH", FC_WRITE_MULTIPLE_COILS, address, count)
        return self._build_response(transaction_id, unit_id, response_pdu)

    def _handle_write_multiple_registers(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Handle Write Multiple Registers (FC 0x10) request."""
        address = struct.unpack(">H", pdu[1:3])[0]
        count = struct.unpack(">H", pdu[3:5])[0]
        _ = pdu[5]  # byte_count (unused)

        values = []
        for i in range(count):
            offset = 6 + i * 2
            if offset + 2 <= len(pdu):
                value = struct.unpack(">H", pdu[offset : offset + 2])[0]
                values.append(value)

        self._datastore.set_holding_registers(address, values)

        response_pdu = struct.pack(">BHH", FC_WRITE_MULTIPLE_REGISTERS, address, count)
        return self._build_response(transaction_id, unit_id, response_pdu)

    def _build_response(
        self,
        transaction_id: int,
        unit_id: int,
        pdu: bytes,
    ) -> bytes:
        """Build a Modbus TCP response frame.

        Args:
            transaction_id: Transaction identifier.
            unit_id: Unit identifier.
            pdu: Protocol Data Unit.

        Returns:
            Complete Modbus TCP frame.
        """
        length = len(pdu) + 1  # PDU + Unit ID
        header = encode_mbap_header(transaction_id, length, unit_id)
        return header + pdu

    def _build_error_response(
        self,
        transaction_id: int,
        unit_id: int,
        function_code: int,
        exception_code: int,
    ) -> bytes:
        """Build a Modbus error response.

        Args:
            transaction_id: Transaction identifier.
            unit_id: Unit identifier.
            function_code: Original function code.
            exception_code: Exception code.

        Returns:
            Error response frame.
        """
        error_pdu = bytes([function_code | 0x80, exception_code])
        return self._build_response(transaction_id, unit_id, error_pdu)

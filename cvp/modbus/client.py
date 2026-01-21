# -*- coding: utf-8 -*-

import socket
import threading
import time
from typing import List, Optional

from cvp.logging.loggers import modbus_logger as logger
from cvp.modbus.exceptions import (
    ModbusConnectionError,
    ModbusProtocolError,
    ModbusSlaveError,
    ModbusTimeoutError,
)
from cvp.modbus.protocol import (
    FC_READ_COILS,
    FC_READ_DISCRETE_INPUTS,
    FC_READ_HOLDING_REGISTERS,
    FC_READ_INPUT_REGISTERS,
    MBAP_HEADER_SIZE,
    decode_mbap_header,
    decode_read_coils_response,
    decode_read_registers_response,
    encode_read_request,
    encode_write_multiple_coils_request,
    encode_write_multiple_registers_request,
    encode_write_single_coil_request,
    encode_write_single_register_request,
    get_exception_code,
    is_error_response,
)


class ModbusTcpClient:
    """Modbus TCP client with threading model and auto-reconnect support."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 502,
        unit_id: int = 1,
        timeout: float = 5.0,
        reconnect_interval: float = 5.0,
    ):
        """Initialize the Modbus TCP client.

        Args:
            host: Server host address.
            port: Server port (default: 502).
            unit_id: Unit identifier (default: 1).
            timeout: Socket timeout in seconds (default: 5.0).
            reconnect_interval: Auto-reconnect interval in seconds (default: 5.0).
        """
        self._host = host
        self._port = port
        self._unit_id = unit_id
        self._timeout = timeout
        self._reconnect_interval = reconnect_interval

        self._socket: Optional[socket.socket] = None
        self._running = False
        self._connected = False
        self._lock = threading.Lock()
        self._transaction_id = 0
        self._reconnect_thread: Optional[threading.Thread] = None

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
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_running(self) -> bool:
        return self._running

    def _next_transaction_id(self) -> int:
        """Get the next transaction ID."""
        self._transaction_id = (self._transaction_id + 1) & 0xFFFF
        return self._transaction_id

    def connect(self) -> bool:
        """Connect to the Modbus server.

        Returns:
            True if connection succeeded, False otherwise.
        """
        with self._lock:
            if self._connected:
                return True

            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.settimeout(self._timeout)
                self._socket.connect((self._host, self._port))
                self._connected = True
                logger.info(f"Connected to Modbus server: {self._host}:{self._port}")
                return True
            except Exception as e:
                logger.error(f"Failed to connect to Modbus server: {e}")
                self._cleanup_socket()
                return False

    def disconnect(self) -> None:
        """Disconnect from the Modbus server."""
        with self._lock:
            self._connected = False
            self._cleanup_socket()
            logger.info("Disconnected from Modbus server")

    def _cleanup_socket(self) -> None:
        """Clean up the socket."""
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

    def start(self) -> None:
        """Start the client with auto-reconnect."""
        if self._running:
            logger.warning("Client is already running")
            return

        self._running = True

        # Initial connection
        self.connect()

        # Start reconnect thread
        self._reconnect_thread = threading.Thread(
            target=self._reconnect_loop,
            name="ModbusReconnectThread",
            daemon=True,
        )
        self._reconnect_thread.start()

        logger.info("Modbus client started")

    def stop(self) -> None:
        """Stop the client and disconnect."""
        if not self._running:
            logger.warning("Client is not running")
            return

        self._running = False
        self.disconnect()

        if self._reconnect_thread:
            self._reconnect_thread.join(timeout=5.0)

        logger.info("Modbus client stopped")

    def _reconnect_loop(self) -> None:
        """Auto-reconnect loop (runs in separate thread)."""
        while self._running:
            if not self._connected:
                logger.info(f"Reconnecting in {self._reconnect_interval} seconds...")
                time.sleep(self._reconnect_interval)

                if not self._running:
                    break

                self.connect()
            else:
                time.sleep(1.0)

    def _send_request(self, request: bytes) -> bytes:
        """Send a request and receive response.

        Args:
            request: Request frame to send.

        Returns:
            Response frame.

        Raises:
            ModbusConnectionError: If not connected.
            ModbusTimeoutError: If timeout occurs.
            ModbusProtocolError: If protocol error occurs.
        """
        with self._lock:
            if not self._connected or not self._socket:
                raise ModbusConnectionError("Not connected to Modbus server")

            try:
                self._socket.send(request)

                # Receive MBAP header
                header = self._recv_exact(MBAP_HEADER_SIZE)
                if not header:
                    self._connected = False
                    raise ModbusConnectionError("Connection closed by server")

                transaction_id, protocol_id, length, unit_id = decode_mbap_header(
                    header
                )

                if protocol_id != 0:
                    raise ModbusProtocolError(f"Invalid protocol ID: {protocol_id}")

                # Receive PDU
                pdu_length = length - 1
                pdu = self._recv_exact(pdu_length)
                if not pdu:
                    self._connected = False
                    raise ModbusConnectionError("Connection closed by server")

                return header + pdu

            except socket.timeout:
                raise ModbusTimeoutError("Request timed out")
            except (ModbusConnectionError, ModbusTimeoutError, ModbusProtocolError):
                raise
            except Exception as e:
                self._connected = False
                raise ModbusConnectionError(f"Communication error: {e}")

    def _recv_exact(self, length: int) -> Optional[bytes]:
        """Receive exactly the specified number of bytes.

        Args:
            length: Number of bytes to receive.

        Returns:
            Received data or None if connection closed.
        """
        if not self._socket:
            return None

        data = bytearray()
        while len(data) < length:
            chunk = self._socket.recv(length - len(data))
            if not chunk:
                return None
            data.extend(chunk)
        return bytes(data)

    def _check_error_response(self, pdu: bytes, expected_fc: int) -> None:
        """Check if response is an error response.

        Args:
            pdu: Response PDU.
            expected_fc: Expected function code.

        Raises:
            ModbusSlaveError: If response indicates an error.
            ModbusProtocolError: If response function code is unexpected.
        """
        function_code = pdu[0]

        if is_error_response(function_code):
            original_fc = function_code & 0x7F
            exception_code = get_exception_code(pdu)
            raise ModbusSlaveError(original_fc, exception_code)

        if function_code != expected_fc:
            raise ModbusProtocolError(
                f"Unexpected function code: {function_code}, expected {expected_fc}"
            )

    def read_coils(self, address: int, count: int) -> List[bool]:
        """Read coils (FC 0x01).

        Args:
            address: Starting address.
            count: Number of coils to read.

        Returns:
            List of coil values.
        """
        transaction_id = self._next_transaction_id()
        request = encode_read_request(
            transaction_id, self._unit_id, FC_READ_COILS, address, count
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_READ_COILS)

        return decode_read_coils_response(pdu)[:count]

    def read_discrete_inputs(self, address: int, count: int) -> List[bool]:
        """Read discrete inputs (FC 0x02).

        Args:
            address: Starting address.
            count: Number of discrete inputs to read.

        Returns:
            List of discrete input values.
        """
        transaction_id = self._next_transaction_id()
        request = encode_read_request(
            transaction_id, self._unit_id, FC_READ_DISCRETE_INPUTS, address, count
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_READ_DISCRETE_INPUTS)

        return decode_read_coils_response(pdu)[:count]

    def read_holding_registers(self, address: int, count: int) -> List[int]:
        """Read holding registers (FC 0x03).

        Args:
            address: Starting address.
            count: Number of registers to read.

        Returns:
            List of register values.
        """
        transaction_id = self._next_transaction_id()
        request = encode_read_request(
            transaction_id, self._unit_id, FC_READ_HOLDING_REGISTERS, address, count
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_READ_HOLDING_REGISTERS)

        return decode_read_registers_response(pdu)

    def read_input_registers(self, address: int, count: int) -> List[int]:
        """Read input registers (FC 0x04).

        Args:
            address: Starting address.
            count: Number of registers to read.

        Returns:
            List of register values.
        """
        transaction_id = self._next_transaction_id()
        request = encode_read_request(
            transaction_id, self._unit_id, FC_READ_INPUT_REGISTERS, address, count
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_READ_INPUT_REGISTERS)

        return decode_read_registers_response(pdu)

    def write_single_coil(self, address: int, value: bool) -> bool:
        """Write a single coil (FC 0x05).

        Args:
            address: Coil address.
            value: Coil value.

        Returns:
            True if write succeeded.
        """
        from cvp.modbus.protocol import FC_WRITE_SINGLE_COIL

        transaction_id = self._next_transaction_id()
        request = encode_write_single_coil_request(
            transaction_id, self._unit_id, address, value
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_WRITE_SINGLE_COIL)

        return True

    def write_single_register(self, address: int, value: int) -> bool:
        """Write a single register (FC 0x06).

        Args:
            address: Register address.
            value: Register value.

        Returns:
            True if write succeeded.
        """
        from cvp.modbus.protocol import FC_WRITE_SINGLE_REGISTER

        transaction_id = self._next_transaction_id()
        request = encode_write_single_register_request(
            transaction_id, self._unit_id, address, value
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_WRITE_SINGLE_REGISTER)

        return True

    def write_multiple_coils(self, address: int, values: List[bool]) -> bool:
        """Write multiple coils (FC 0x0F).

        Args:
            address: Starting address.
            values: List of coil values.

        Returns:
            True if write succeeded.
        """
        from cvp.modbus.protocol import FC_WRITE_MULTIPLE_COILS

        transaction_id = self._next_transaction_id()
        request = encode_write_multiple_coils_request(
            transaction_id, self._unit_id, address, values
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_WRITE_MULTIPLE_COILS)

        return True

    def write_multiple_registers(self, address: int, values: List[int]) -> bool:
        """Write multiple registers (FC 0x10).

        Args:
            address: Starting address.
            values: List of register values.

        Returns:
            True if write succeeded.
        """
        from cvp.modbus.protocol import FC_WRITE_MULTIPLE_REGISTERS

        transaction_id = self._next_transaction_id()
        request = encode_write_multiple_registers_request(
            transaction_id, self._unit_id, address, values
        )
        response = self._send_request(request)

        pdu = response[MBAP_HEADER_SIZE:]
        self._check_error_response(pdu, FC_WRITE_MULTIPLE_REGISTERS)

        return True

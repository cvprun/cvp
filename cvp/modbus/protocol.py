# -*- coding: utf-8 -*-

import struct
from typing import Final, List, Tuple

# Modbus Function Codes
FC_READ_COILS: Final[int] = 0x01
FC_READ_DISCRETE_INPUTS: Final[int] = 0x02
FC_READ_HOLDING_REGISTERS: Final[int] = 0x03
FC_READ_INPUT_REGISTERS: Final[int] = 0x04
FC_WRITE_SINGLE_COIL: Final[int] = 0x05
FC_WRITE_SINGLE_REGISTER: Final[int] = 0x06
FC_WRITE_MULTIPLE_COILS: Final[int] = 0x0F
FC_WRITE_MULTIPLE_REGISTERS: Final[int] = 0x10

# Modbus Constants
MODBUS_PROTOCOL_ID: Final[int] = 0x0000
COIL_ON: Final[int] = 0xFF00
COIL_OFF: Final[int] = 0x0000

# Limits
MAX_COILS_READ: Final[int] = 2000
MAX_DISCRETE_INPUTS_READ: Final[int] = 2000
MAX_HOLDING_REGISTERS_READ: Final[int] = 125
MAX_INPUT_REGISTERS_READ: Final[int] = 125
MAX_COILS_WRITE: Final[int] = 1968
MAX_REGISTERS_WRITE: Final[int] = 123

# MBAP Header Size: Transaction ID (2) + Protocol ID (2) + Length (2) + Unit ID (1)
MBAP_HEADER_SIZE: Final[int] = 7


def encode_mbap_header(
    transaction_id: int,
    length: int,
    unit_id: int,
) -> bytes:
    """Encode MBAP (Modbus Application Protocol) header.

    Args:
        transaction_id: Transaction identifier (2 bytes).
        length: Length of remaining message including unit ID (2 bytes).
        unit_id: Unit identifier (1 byte).

    Returns:
        Encoded MBAP header (7 bytes).
    """
    return struct.pack(
        ">HHHB",
        transaction_id,
        MODBUS_PROTOCOL_ID,
        length,
        unit_id,
    )


def decode_mbap_header(data: bytes) -> Tuple[int, int, int, int]:
    """Decode MBAP header.

    Args:
        data: Raw MBAP header data (at least 7 bytes).

    Returns:
        Tuple of (transaction_id, protocol_id, length, unit_id).
    """
    return struct.unpack(">HHHB", data[:MBAP_HEADER_SIZE])


def encode_read_request(
    transaction_id: int,
    unit_id: int,
    function_code: int,
    address: int,
    count: int,
) -> bytes:
    """Encode a Modbus read request.

    Args:
        transaction_id: Transaction identifier.
        unit_id: Unit identifier.
        function_code: Modbus function code (0x01-0x04).
        address: Starting address.
        count: Number of items to read.

    Returns:
        Encoded Modbus TCP frame.
    """
    pdu = struct.pack(">BHH", function_code, address, count)
    length = len(pdu) + 1  # PDU + Unit ID
    header = encode_mbap_header(transaction_id, length, unit_id)
    return header + pdu


def encode_write_single_coil_request(
    transaction_id: int,
    unit_id: int,
    address: int,
    value: bool,
) -> bytes:
    """Encode a write single coil request.

    Args:
        transaction_id: Transaction identifier.
        unit_id: Unit identifier.
        address: Coil address.
        value: Coil value (True for ON, False for OFF).

    Returns:
        Encoded Modbus TCP frame.
    """
    coil_value = COIL_ON if value else COIL_OFF
    pdu = struct.pack(">BHH", FC_WRITE_SINGLE_COIL, address, coil_value)
    length = len(pdu) + 1
    header = encode_mbap_header(transaction_id, length, unit_id)
    return header + pdu


def encode_write_single_register_request(
    transaction_id: int,
    unit_id: int,
    address: int,
    value: int,
) -> bytes:
    """Encode a write single register request.

    Args:
        transaction_id: Transaction identifier.
        unit_id: Unit identifier.
        address: Register address.
        value: Register value (0-65535).

    Returns:
        Encoded Modbus TCP frame.
    """
    pdu = struct.pack(">BHH", FC_WRITE_SINGLE_REGISTER, address, value & 0xFFFF)
    length = len(pdu) + 1
    header = encode_mbap_header(transaction_id, length, unit_id)
    return header + pdu


def encode_write_multiple_coils_request(
    transaction_id: int,
    unit_id: int,
    address: int,
    values: List[bool],
) -> bytes:
    """Encode a write multiple coils request.

    Args:
        transaction_id: Transaction identifier.
        unit_id: Unit identifier.
        address: Starting coil address.
        values: List of coil values.

    Returns:
        Encoded Modbus TCP frame.
    """
    count = len(values)
    byte_count = (count + 7) // 8

    coil_bytes = bytearray(byte_count)
    for i, value in enumerate(values):
        if value:
            coil_bytes[i // 8] |= 1 << (i % 8)

    pdu = struct.pack(">BHHB", FC_WRITE_MULTIPLE_COILS, address, count, byte_count)
    pdu += bytes(coil_bytes)

    length = len(pdu) + 1
    header = encode_mbap_header(transaction_id, length, unit_id)
    return header + pdu


def encode_write_multiple_registers_request(
    transaction_id: int,
    unit_id: int,
    address: int,
    values: List[int],
) -> bytes:
    """Encode a write multiple registers request.

    Args:
        transaction_id: Transaction identifier.
        unit_id: Unit identifier.
        address: Starting register address.
        values: List of register values.

    Returns:
        Encoded Modbus TCP frame.
    """
    count = len(values)
    byte_count = count * 2

    pdu = struct.pack(">BHHB", FC_WRITE_MULTIPLE_REGISTERS, address, count, byte_count)
    for value in values:
        pdu += struct.pack(">H", value & 0xFFFF)

    length = len(pdu) + 1
    header = encode_mbap_header(transaction_id, length, unit_id)
    return header + pdu


def decode_read_coils_response(data: bytes) -> List[bool]:
    """Decode a read coils/discrete inputs response.

    Args:
        data: Response PDU (after MBAP header, starting from function code).

    Returns:
        List of coil/discrete input values.
    """
    byte_count = data[1]
    coil_data = data[2 : 2 + byte_count]

    result = []
    for byte_val in coil_data:
        for bit in range(8):
            result.append(bool(byte_val & (1 << bit)))

    return result


def decode_read_registers_response(data: bytes) -> List[int]:
    """Decode a read registers response.

    Args:
        data: Response PDU (after MBAP header, starting from function code).

    Returns:
        List of register values.
    """
    byte_count = data[1]
    register_count = byte_count // 2

    result = []
    for i in range(register_count):
        offset = 2 + i * 2
        value = struct.unpack(">H", data[offset : offset + 2])[0]
        result.append(value)

    return result


def is_error_response(function_code: int) -> bool:
    """Check if the function code indicates an error response.

    Args:
        function_code: Received function code.

    Returns:
        True if this is an error response (high bit set).
    """
    return bool(function_code & 0x80)


def get_exception_code(data: bytes) -> int:
    """Extract the exception code from an error response.

    Args:
        data: Response PDU (after MBAP header).

    Returns:
        Exception code.
    """
    return data[1]

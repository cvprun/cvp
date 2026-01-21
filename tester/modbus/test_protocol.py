# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.modbus.protocol import (
    COIL_OFF,
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
    MODBUS_PROTOCOL_ID,
    decode_mbap_header,
    decode_read_coils_response,
    decode_read_registers_response,
    encode_mbap_header,
    encode_read_request,
    encode_write_multiple_coils_request,
    encode_write_multiple_registers_request,
    encode_write_single_coil_request,
    encode_write_single_register_request,
    get_exception_code,
    is_error_response,
)


class TestMbapHeader(TestCase):
    def test_encode_mbap_header(self) -> None:
        header = encode_mbap_header(
            transaction_id=0x0001,
            length=6,
            unit_id=1,
        )
        self.assertEqual(len(header), MBAP_HEADER_SIZE)
        self.assertEqual(header[0:2], b"\x00\x01")  # Transaction ID
        self.assertEqual(header[2:4], b"\x00\x00")  # Protocol ID
        self.assertEqual(header[4:6], b"\x00\x06")  # Length
        self.assertEqual(header[6], 1)  # Unit ID

    def test_decode_mbap_header(self) -> None:
        header = b"\x00\x01\x00\x00\x00\x06\x01"
        tid, pid, length, uid = decode_mbap_header(header)
        self.assertEqual(tid, 1)
        self.assertEqual(pid, MODBUS_PROTOCOL_ID)
        self.assertEqual(length, 6)
        self.assertEqual(uid, 1)

    def test_roundtrip(self) -> None:
        original_tid = 0x1234
        original_length = 0x0A
        original_uid = 0x05

        encoded = encode_mbap_header(original_tid, original_length, original_uid)
        tid, pid, length, uid = decode_mbap_header(encoded)

        self.assertEqual(tid, original_tid)
        self.assertEqual(pid, MODBUS_PROTOCOL_ID)
        self.assertEqual(length, original_length)
        self.assertEqual(uid, original_uid)


class TestReadRequests(TestCase):
    def test_encode_read_coils_request(self) -> None:
        frame = encode_read_request(
            transaction_id=1,
            unit_id=1,
            function_code=FC_READ_COILS,
            address=0,
            count=10,
        )
        self.assertEqual(len(frame), 12)  # 7 (MBAP) + 5 (PDU)
        self.assertEqual(frame[7], FC_READ_COILS)

    def test_encode_read_discrete_inputs_request(self) -> None:
        frame = encode_read_request(
            transaction_id=1,
            unit_id=1,
            function_code=FC_READ_DISCRETE_INPUTS,
            address=100,
            count=16,
        )
        self.assertEqual(frame[7], FC_READ_DISCRETE_INPUTS)

    def test_encode_read_holding_registers_request(self) -> None:
        frame = encode_read_request(
            transaction_id=1,
            unit_id=1,
            function_code=FC_READ_HOLDING_REGISTERS,
            address=0,
            count=10,
        )
        self.assertEqual(frame[7], FC_READ_HOLDING_REGISTERS)

    def test_encode_read_input_registers_request(self) -> None:
        frame = encode_read_request(
            transaction_id=1,
            unit_id=1,
            function_code=FC_READ_INPUT_REGISTERS,
            address=0,
            count=5,
        )
        self.assertEqual(frame[7], FC_READ_INPUT_REGISTERS)


class TestWriteRequests(TestCase):
    def test_encode_write_single_coil_on(self) -> None:
        frame = encode_write_single_coil_request(
            transaction_id=1,
            unit_id=1,
            address=0,
            value=True,
        )
        self.assertEqual(frame[7], FC_WRITE_SINGLE_COIL)
        # Check coil value is ON (0xFF00)
        coil_value = (frame[10] << 8) | frame[11]
        self.assertEqual(coil_value, COIL_ON)

    def test_encode_write_single_coil_off(self) -> None:
        frame = encode_write_single_coil_request(
            transaction_id=1,
            unit_id=1,
            address=0,
            value=False,
        )
        coil_value = (frame[10] << 8) | frame[11]
        self.assertEqual(coil_value, COIL_OFF)

    def test_encode_write_single_register(self) -> None:
        frame = encode_write_single_register_request(
            transaction_id=1,
            unit_id=1,
            address=0,
            value=12345,
        )
        self.assertEqual(frame[7], FC_WRITE_SINGLE_REGISTER)
        reg_value = (frame[10] << 8) | frame[11]
        self.assertEqual(reg_value, 12345)

    def test_encode_write_multiple_coils(self) -> None:
        values = [True, False, True, True, False, False, True, False, True]
        frame = encode_write_multiple_coils_request(
            transaction_id=1,
            unit_id=1,
            address=0,
            values=values,
        )
        self.assertEqual(frame[7], FC_WRITE_MULTIPLE_COILS)

    def test_encode_write_multiple_registers(self) -> None:
        values = [100, 200, 300]
        frame = encode_write_multiple_registers_request(
            transaction_id=1,
            unit_id=1,
            address=0,
            values=values,
        )
        self.assertEqual(frame[7], FC_WRITE_MULTIPLE_REGISTERS)


class TestResponseDecoding(TestCase):
    def test_decode_read_coils_response(self) -> None:
        # Response: FC=0x01, byte_count=2, data=0xCD 0x6B
        # Binary: 11001101 01101011
        pdu = bytes([FC_READ_COILS, 2, 0xCD, 0x6B])
        result = decode_read_coils_response(pdu)
        # First byte 0xCD = 11001101 -> bits 0-7: T,F,T,T,F,F,T,T
        expected_first_8 = [True, False, True, True, False, False, True, True]
        self.assertEqual(result[:8], expected_first_8)

    def test_decode_read_registers_response(self) -> None:
        # Response: FC=0x03, byte_count=6, data: 3 registers
        pdu = bytes([FC_READ_HOLDING_REGISTERS, 6, 0x00, 0x64, 0x00, 0xC8, 0x01, 0x2C])
        result = decode_read_registers_response(pdu)
        self.assertEqual(result, [100, 200, 300])


class TestErrorHandling(TestCase):
    def test_is_error_response(self) -> None:
        self.assertTrue(is_error_response(0x81))  # FC 0x01 error
        self.assertTrue(is_error_response(0x83))  # FC 0x03 error
        self.assertFalse(is_error_response(0x01))  # Normal response
        self.assertFalse(is_error_response(0x03))  # Normal response

    def test_get_exception_code(self) -> None:
        error_pdu = bytes([0x81, 0x02])  # Error FC, illegal data address
        self.assertEqual(get_exception_code(error_pdu), 0x02)


if __name__ == "__main__":
    main()

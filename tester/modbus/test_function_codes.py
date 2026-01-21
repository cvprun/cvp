# -*- coding: utf-8 -*-

import time
from typing import ClassVar
from unittest import TestCase, main

from cvp.modbus.client import ModbusTcpClient
from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.server import ModbusTcpServer


class TestFunctionCodes(TestCase):
    datastore: ClassVar[ModbusDataStore]
    server: ClassVar[ModbusTcpServer]

    @classmethod
    def setUpClass(cls) -> None:
        cls.datastore = ModbusDataStore()
        cls.server = ModbusTcpServer(
            host="localhost",
            port=15050,
            datastore=cls.datastore,
            unit_id=1,
        )
        cls.server.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.stop()

    def setUp(self) -> None:
        self.client = ModbusTcpClient(
            host="localhost",
            port=15050,
            unit_id=1,
            timeout=5.0,
        )
        self.assertTrue(self.client.connect())
        self.datastore.reset()

    def tearDown(self) -> None:
        self.client.disconnect()


class TestFC01ReadCoils(TestFunctionCodes):
    def test_read_single_coil(self) -> None:
        self.datastore.set_coil(0, True)
        result = self.client.read_coils(0, 1)
        self.assertEqual(result, [True])

    def test_read_multiple_coils(self) -> None:
        self.datastore.set_coils(0, [True, False, True, True, False, False, True, True])
        result = self.client.read_coils(0, 8)
        self.assertEqual(result, [True, False, True, True, False, False, True, True])

    def test_read_coils_across_byte_boundary(self) -> None:
        # 10 coils spans 2 bytes
        values = [True] * 10
        self.datastore.set_coils(0, values)
        result = self.client.read_coils(0, 10)
        self.assertEqual(result, values)

    def test_read_coils_at_offset(self) -> None:
        self.datastore.set_coils(100, [False, True, True])
        result = self.client.read_coils(100, 3)
        self.assertEqual(result, [False, True, True])


class TestFC02ReadDiscreteInputs(TestFunctionCodes):
    def test_read_single_input(self) -> None:
        self.datastore.set_discrete_inputs(0, [True])
        result = self.client.read_discrete_inputs(0, 1)
        self.assertEqual(result, [True])

    def test_read_multiple_inputs(self) -> None:
        values = [True, True, False, True, False]
        self.datastore.set_discrete_inputs(0, values)
        result = self.client.read_discrete_inputs(0, 5)
        self.assertEqual(result, values)


class TestFC03ReadHoldingRegisters(TestFunctionCodes):
    def test_read_single_register(self) -> None:
        self.datastore.set_holding_register(0, 42)
        result = self.client.read_holding_registers(0, 1)
        self.assertEqual(result, [42])

    def test_read_multiple_registers(self) -> None:
        self.datastore.set_holding_registers(0, [100, 200, 300, 400, 500])
        result = self.client.read_holding_registers(0, 5)
        self.assertEqual(result, [100, 200, 300, 400, 500])

    def test_read_max_value_register(self) -> None:
        self.datastore.set_holding_register(0, 65535)
        result = self.client.read_holding_registers(0, 1)
        self.assertEqual(result, [65535])


class TestFC04ReadInputRegisters(TestFunctionCodes):
    def test_read_single_input_register(self) -> None:
        self.datastore.set_input_registers(0, [9999])
        result = self.client.read_input_registers(0, 1)
        self.assertEqual(result, [9999])

    def test_read_multiple_input_registers(self) -> None:
        values = [1111, 2222, 3333]
        self.datastore.set_input_registers(10, values)
        result = self.client.read_input_registers(10, 3)
        self.assertEqual(result, values)


class TestFC05WriteSingleCoil(TestFunctionCodes):
    def test_write_coil_on(self) -> None:
        self.client.write_single_coil(0, True)
        result = self.datastore.get_coils(0, 1)
        self.assertEqual(result, [True])

    def test_write_coil_off(self) -> None:
        self.datastore.set_coil(0, True)
        self.client.write_single_coil(0, False)
        result = self.datastore.get_coils(0, 1)
        self.assertEqual(result, [False])

    def test_write_coil_at_offset(self) -> None:
        self.client.write_single_coil(500, True)
        result = self.datastore.get_coils(500, 1)
        self.assertEqual(result, [True])


class TestFC06WriteSingleRegister(TestFunctionCodes):
    def test_write_register(self) -> None:
        self.client.write_single_register(0, 12345)
        result = self.datastore.get_holding_registers(0, 1)
        self.assertEqual(result, [12345])

    def test_write_max_value(self) -> None:
        self.client.write_single_register(0, 65535)
        result = self.datastore.get_holding_registers(0, 1)
        self.assertEqual(result, [65535])

    def test_write_register_at_offset(self) -> None:
        self.client.write_single_register(1000, 9876)
        result = self.datastore.get_holding_registers(1000, 1)
        self.assertEqual(result, [9876])


class TestFC0FWriteMultipleCoils(TestFunctionCodes):
    def test_write_few_coils(self) -> None:
        values = [True, False, True]
        self.client.write_multiple_coils(0, values)
        result = self.datastore.get_coils(0, 3)
        self.assertEqual(result, values)

    def test_write_coils_across_byte_boundary(self) -> None:
        values = [True, False] * 6  # 12 coils
        self.client.write_multiple_coils(0, values)
        result = self.datastore.get_coils(0, 12)
        self.assertEqual(result, values)

    def test_write_coils_at_offset(self) -> None:
        values = [False, True, True, False]
        self.client.write_multiple_coils(200, values)
        result = self.datastore.get_coils(200, 4)
        self.assertEqual(result, values)


class TestFC10WriteMultipleRegisters(TestFunctionCodes):
    def test_write_few_registers(self) -> None:
        values = [111, 222, 333]
        self.client.write_multiple_registers(0, values)
        result = self.datastore.get_holding_registers(0, 3)
        self.assertEqual(result, values)

    def test_write_many_registers(self) -> None:
        values = list(range(10))
        self.client.write_multiple_registers(0, values)
        result = self.datastore.get_holding_registers(0, 10)
        self.assertEqual(result, values)

    def test_write_registers_at_offset(self) -> None:
        values = [5000, 6000, 7000]
        self.client.write_multiple_registers(500, values)
        result = self.datastore.get_holding_registers(500, 3)
        self.assertEqual(result, values)


if __name__ == "__main__":
    main()

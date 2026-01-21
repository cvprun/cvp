# -*- coding: utf-8 -*-

import time
from unittest import TestCase, main

from cvp.modbus.client import ModbusTcpClient
from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.server import ModbusTcpServer


class TestServerClientIntegration(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.datastore = ModbusDataStore()
        cls.server = ModbusTcpServer(
            host="localhost",
            port=15040,
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
            port=15040,
            unit_id=1,
            timeout=5.0,
        )
        self.assertTrue(self.client.connect())
        self.datastore.reset()

    def tearDown(self) -> None:
        self.client.disconnect()

    def test_read_holding_registers(self) -> None:
        self.datastore.set_holding_registers(0, [100, 200, 300])
        result = self.client.read_holding_registers(0, 3)
        self.assertEqual(result, [100, 200, 300])

    def test_read_input_registers(self) -> None:
        self.datastore.set_input_registers(10, [1000, 2000, 3000])
        result = self.client.read_input_registers(10, 3)
        self.assertEqual(result, [1000, 2000, 3000])

    def test_read_coils(self) -> None:
        self.datastore.set_coils(0, [True, False, True, True, False])
        result = self.client.read_coils(0, 5)
        self.assertEqual(result, [True, False, True, True, False])

    def test_read_discrete_inputs(self) -> None:
        self.datastore.set_discrete_inputs(5, [False, True, True, False])
        result = self.client.read_discrete_inputs(5, 4)
        self.assertEqual(result, [False, True, True, False])

    def test_write_single_coil(self) -> None:
        self.client.write_single_coil(10, True)
        result = self.datastore.get_coils(10, 1)
        self.assertEqual(result, [True])

    def test_write_single_register(self) -> None:
        self.client.write_single_register(20, 12345)
        result = self.datastore.get_holding_registers(20, 1)
        self.assertEqual(result, [12345])

    def test_write_multiple_coils(self) -> None:
        values = [True, False, True, True, False, False, True]
        self.client.write_multiple_coils(0, values)
        result = self.datastore.get_coils(0, 7)
        self.assertEqual(result, values)

    def test_write_multiple_registers(self) -> None:
        values = [100, 200, 300, 400, 500]
        self.client.write_multiple_registers(0, values)
        result = self.datastore.get_holding_registers(0, 5)
        self.assertEqual(result, values)

    def test_roundtrip_registers(self) -> None:
        values = [111, 222, 333]
        self.client.write_multiple_registers(100, values)
        result = self.client.read_holding_registers(100, 3)
        self.assertEqual(result, values)

    def test_roundtrip_coils(self) -> None:
        values = [True, True, False, True, False]
        self.client.write_multiple_coils(50, values)
        result = self.client.read_coils(50, 5)
        self.assertEqual(result, values)


class TestServerClientReconnection(TestCase):
    def test_reconnection(self) -> None:
        datastore = ModbusDataStore()
        server = ModbusTcpServer(
            host="localhost",
            port=15041,
            datastore=datastore,
            unit_id=1,
        )
        server.start()
        time.sleep(0.1)

        client = ModbusTcpClient(
            host="localhost",
            port=15041,
            timeout=2.0,
            reconnect_interval=1.0,
        )
        client.start()
        time.sleep(0.1)

        self.assertTrue(client.is_connected)

        # Stop server
        server.stop()
        time.sleep(0.2)

        # Restart server
        server.start()
        time.sleep(2.5)  # Wait for reconnection

        self.assertTrue(client.is_connected)

        client.stop()
        server.stop()


if __name__ == "__main__":
    main()

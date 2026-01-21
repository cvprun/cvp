# -*- coding: utf-8 -*-

import socket
import time
from unittest import TestCase, main

from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.server import ModbusTcpServer


class TestModbusTcpServerBasic(TestCase):
    def test_server_start_stop(self) -> None:
        server = ModbusTcpServer(host="localhost", port=15020)
        self.assertFalse(server.is_running)

        server.start()
        self.assertTrue(server.is_running)

        server.stop()
        self.assertFalse(server.is_running)

    def test_server_properties(self) -> None:
        datastore = ModbusDataStore()
        server = ModbusTcpServer(
            host="127.0.0.1",
            port=15021,
            datastore=datastore,
            unit_id=5,
        )
        self.assertEqual(server.host, "127.0.0.1")
        self.assertEqual(server.port, 15021)
        self.assertEqual(server.unit_id, 5)
        self.assertIs(server.datastore, datastore)

    def test_server_start_twice(self) -> None:
        server = ModbusTcpServer(host="localhost", port=15022)
        server.start()
        try:
            server.start()  # Should not raise, just warn
            self.assertTrue(server.is_running)
        finally:
            server.stop()

    def test_server_stop_without_start(self) -> None:
        server = ModbusTcpServer(host="localhost", port=15023)
        server.stop()  # Should not raise, just warn
        self.assertFalse(server.is_running)


class TestModbusTcpServerConnection(TestCase):
    def setUp(self) -> None:
        self.datastore = ModbusDataStore()
        self.server = ModbusTcpServer(
            host="localhost",
            port=15024,
            datastore=self.datastore,
            unit_id=1,
        )
        self.server.start()
        time.sleep(0.1)

    def tearDown(self) -> None:
        self.server.stop()

    def test_client_connection(self) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("localhost", 15024))
            time.sleep(0.1)
            self.assertEqual(self.server.client_count, 1)
        finally:
            client.close()
            time.sleep(0.1)

    def test_multiple_client_connections(self) -> None:
        clients = []
        try:
            for _ in range(3):
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("localhost", 15024))
                clients.append(client)
            time.sleep(0.1)
            self.assertEqual(self.server.client_count, 3)
        finally:
            for client in clients:
                client.close()
            time.sleep(0.1)


if __name__ == "__main__":
    main()

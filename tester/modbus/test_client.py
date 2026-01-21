# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.modbus.client import ModbusTcpClient


class TestModbusTcpClientBasic(TestCase):
    def test_client_properties(self) -> None:
        client = ModbusTcpClient(
            host="127.0.0.1",
            port=15030,
            unit_id=5,
            timeout=10.0,
            reconnect_interval=3.0,
        )
        self.assertEqual(client.host, "127.0.0.1")
        self.assertEqual(client.port, 15030)
        self.assertEqual(client.unit_id, 5)
        self.assertFalse(client.is_connected)
        self.assertFalse(client.is_running)

    def test_client_connect_no_server(self) -> None:
        client = ModbusTcpClient(host="localhost", port=15031, timeout=1.0)
        result = client.connect()
        self.assertFalse(result)
        self.assertFalse(client.is_connected)

    def test_client_disconnect_not_connected(self) -> None:
        client = ModbusTcpClient(host="localhost", port=15032)
        client.disconnect()  # Should not raise
        self.assertFalse(client.is_connected)


class TestModbusTcpClientStartStop(TestCase):
    def test_start_stop_no_server(self) -> None:
        client = ModbusTcpClient(
            host="localhost",
            port=15033,
            timeout=1.0,
            reconnect_interval=1.0,
        )

        client.start()
        self.assertTrue(client.is_running)
        self.assertFalse(client.is_connected)

        client.stop()
        self.assertFalse(client.is_running)

    def test_start_twice(self) -> None:
        client = ModbusTcpClient(host="localhost", port=15034, timeout=1.0)
        client.start()
        try:
            client.start()  # Should not raise, just warn
            self.assertTrue(client.is_running)
        finally:
            client.stop()

    def test_stop_without_start(self) -> None:
        client = ModbusTcpClient(host="localhost", port=15035)
        client.stop()  # Should not raise, just warn
        self.assertFalse(client.is_running)


if __name__ == "__main__":
    main()

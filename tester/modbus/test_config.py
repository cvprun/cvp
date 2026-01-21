# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.modbus.config import ModbusDeviceConfig, ModbusKey, ModbusRole


class TestModbusDeviceConfig(TestCase):
    def test_default_values(self) -> None:
        config = ModbusDeviceConfig()
        self.assertIsNotNone(config.uuid)
        self.assertEqual(config.name, "")
        self.assertEqual(config.role, ModbusRole.client)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 502)
        self.assertEqual(config.unit_id, 1)
        self.assertEqual(config.timeout, 5.0)
        self.assertEqual(config.reconnect_interval, 5.0)
        self.assertFalse(config.autostart)

    def test_custom_values(self) -> None:
        config = ModbusDeviceConfig(
            uuid="test-uuid",
            name="Test Device",
            role=ModbusRole.server,
            host="192.168.1.100",
            port=5020,
            unit_id=5,
            timeout=10.0,
            reconnect_interval=3.0,
            autostart=True,
        )
        self.assertEqual(config.uuid, "test-uuid")
        self.assertEqual(config.name, "Test Device")
        self.assertEqual(config.role, ModbusRole.server)
        self.assertEqual(config.host, "192.168.1.100")
        self.assertEqual(config.port, 5020)
        self.assertEqual(config.unit_id, 5)
        self.assertEqual(config.timeout, 10.0)
        self.assertEqual(config.reconnect_interval, 3.0)
        self.assertTrue(config.autostart)

    def test_key_property(self) -> None:
        config = ModbusDeviceConfig(uuid="my-uuid")
        self.assertEqual(config.key, ModbusKey("my-uuid"))

    def test_key_setter(self) -> None:
        config = ModbusDeviceConfig()
        config.key = ModbusKey("new-key")
        self.assertEqual(config.uuid, "new-key")

    def test_is_server(self) -> None:
        server_config = ModbusDeviceConfig(role=ModbusRole.server)
        client_config = ModbusDeviceConfig(role=ModbusRole.client)

        self.assertTrue(server_config.is_server)
        self.assertFalse(server_config.is_client)
        self.assertFalse(client_config.is_server)
        self.assertTrue(client_config.is_client)


class TestModbusRole(TestCase):
    def test_role_values(self) -> None:
        self.assertEqual(ModbusRole.server, "server")
        self.assertEqual(ModbusRole.client, "client")


if __name__ == "__main__":
    main()

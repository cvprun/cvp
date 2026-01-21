# -*- coding: utf-8 -*-

import tempfile
import time
from pathlib import Path
from unittest import TestCase, main

from cvp.modbus.config import ModbusRole
from cvp.modbus.manager import ModbusManager
from cvp.resources.subdirs.modbus import ModbusPath


class TestModbusManager(TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.path = ModbusPath(self.temp_dir)
        self.manager = ModbusManager(self.path)

    def tearDown(self) -> None:
        self.manager.shutdown_all()

    def test_add_server_device(self) -> None:
        key, config = self.manager.add_device(
            name="Test Server",
            role=ModbusRole.server,
            host="localhost",
            port=15060,
            unit_id=1,
        )
        self.assertIn(key, self.manager)
        self.assertEqual(config.name, "Test Server")
        self.assertTrue(config.is_server)

    def test_add_client_device(self) -> None:
        key, config = self.manager.add_device(
            name="Test Client",
            role=ModbusRole.client,
            host="localhost",
            port=15061,
        )
        self.assertIn(key, self.manager)
        self.assertEqual(config.name, "Test Client")
        self.assertTrue(config.is_client)

    def test_start_stop_server(self) -> None:
        key, _ = self.manager.add_device(
            name="Test Server",
            role=ModbusRole.server,
            host="localhost",
            port=15062,
        )
        server = self.manager.start_server(key)
        self.assertTrue(server.is_running)
        self.assertTrue(self.manager.has_server(key))

        self.manager.stop_server(key)
        self.assertFalse(server.is_running)
        self.assertFalse(self.manager.has_server(key))

    def test_connect_disconnect_client(self) -> None:
        # First start a server
        server_key, _ = self.manager.add_device(
            name="Server",
            role=ModbusRole.server,
            host="localhost",
            port=15063,
        )
        self.manager.start_server(server_key)
        time.sleep(0.1)

        # Then connect client
        client_key, _ = self.manager.add_device(
            name="Client",
            role=ModbusRole.client,
            host="localhost",
            port=15063,
        )
        client = self.manager.connect_client(client_key)
        time.sleep(0.1)

        self.assertTrue(client.is_running)
        self.assertTrue(self.manager.has_client(client_key))

        self.manager.disconnect_client(client_key)
        self.assertFalse(client.is_running)
        self.assertFalse(self.manager.has_client(client_key))

    def test_start_server_wrong_role(self) -> None:
        key, _ = self.manager.add_device(
            name="Client",
            role=ModbusRole.client,
        )
        with self.assertRaises(ValueError):
            self.manager.start_server(key)

    def test_connect_client_wrong_role(self) -> None:
        key, _ = self.manager.add_device(
            name="Server",
            role=ModbusRole.server,
        )
        with self.assertRaises(ValueError):
            self.manager.connect_client(key)

    def test_shutdown_all(self) -> None:
        key1, _ = self.manager.add_device(
            name="Server 1",
            role=ModbusRole.server,
            host="localhost",
            port=15064,
        )
        key2, _ = self.manager.add_device(
            name="Server 2",
            role=ModbusRole.server,
            host="localhost",
            port=15065,
        )
        self.manager.start_server(key1)
        self.manager.start_server(key2)

        self.manager.shutdown_all()

        self.assertFalse(self.manager.has_server(key1))
        self.assertFalse(self.manager.has_server(key2))

    def test_remove_device(self) -> None:
        key, _ = self.manager.add_device(
            name="Server",
            role=ModbusRole.server,
            host="localhost",
            port=15066,
        )
        self.manager.start_server(key)

        self.manager.remove_device(key)

        self.assertNotIn(key, self.manager)
        self.assertFalse(self.manager.has_server(key))


class TestModbusManagerPersistence(TestCase):
    def test_config_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = ModbusPath(temp_dir)
            Path(temp_dir).mkdir(parents=True, exist_ok=True)

            manager1 = ModbusManager(path)
            key, config = manager1.add_device(
                name="Persistent Device",
                role=ModbusRole.server,
                host="192.168.1.100",
                port=5020,
                unit_id=5,
            )

            manager2 = ModbusManager(path, reload=True)
            self.assertIn(key, manager2)

            loaded_config = manager2[key]
            self.assertEqual(loaded_config.name, "Persistent Device")
            self.assertEqual(loaded_config.host, "192.168.1.100")
            self.assertEqual(loaded_config.port, 5020)
            self.assertEqual(loaded_config.unit_id, 5)


if __name__ == "__main__":
    main()

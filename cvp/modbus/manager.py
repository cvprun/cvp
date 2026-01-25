# -*- coding: utf-8 -*-

from typing import Dict, Optional, Tuple
from uuid import uuid4

from type_serialize import deserialize, serialize

from cvp.logging.loggers import modbus_logger as logger
from cvp.modbus.client import ModbusTcpClient
from cvp.modbus.config import (
    ModbusDataStoreConfig,
    ModbusDeviceConfig,
    ModbusKey,
    ModbusRole,
)
from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.server import ModbusTcpServer
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.modbus import ModbusPath


class ModbusManager(ResourceManager[ModbusKey, ModbusDeviceConfig]):
    """Manager for Modbus TCP servers and clients."""

    _servers: Dict[ModbusKey, ModbusTcpServer]
    _clients: Dict[ModbusKey, ModbusTcpClient]
    _data_stores: Dict[ModbusKey, ModbusDataStore]
    _datastore_configs: Dict[ModbusKey, ModbusDataStoreConfig]

    def __init__(
        self,
        path: ModbusPath,
        *,
        reload: bool = False,
        raise_errors: bool = False,
    ):
        """Initialize the Modbus manager.

        Args:
            path: Path to Modbus configuration directory.
            reload: Whether to reload configurations from disk.
            raise_errors: Whether to raise errors during loading.
        """
        super().__init__(
            key_type=ModbusKey,
            config_type=ModbusDeviceConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._path = path
        self._datastore_path = path.get_datastore_path()
        self._servers = dict()
        self._clients = dict()
        self._data_stores = dict()
        self._datastore_configs = dict()

        if reload:
            self._load_all_datastore_configs(raise_errors=raise_errors)

    def has_server(self, key: ModbusKey) -> bool:
        """Check if a server exists for the given key."""
        return key in self._servers

    def has_client(self, key: ModbusKey) -> bool:
        """Check if a client exists for the given key."""
        return key in self._clients

    def get_server(self, key: ModbusKey) -> Optional[ModbusTcpServer]:
        """Get a server by key."""
        return self._servers.get(key)

    def get_client(self, key: ModbusKey) -> Optional[ModbusTcpClient]:
        """Get a client by key."""
        return self._clients.get(key)

    def get_datastore(self, key: ModbusKey) -> Optional[ModbusDataStore]:
        """Get a datastore by key."""
        return self._data_stores.get(key)

    def get_datastore_config(self, key: ModbusKey) -> Optional[ModbusDataStoreConfig]:
        """Get a datastore config by key."""
        return self._datastore_configs.get(key)

    def _load_all_datastore_configs(self, *, raise_errors: bool = False) -> None:
        """Load all datastore configs from disk."""
        datastore_path = self._datastore_path
        if not datastore_path.as_path().exists():
            return

        for filename in datastore_path.list_object_filenames():
            key_str = filename.removesuffix(datastore_path.extension)
            key = ModbusKey(key_str)
            try:
                data = datastore_path.read_object(key_str)
                config = deserialize(data, ModbusDataStoreConfig)
                self._datastore_configs[key] = config
                logger.info(f"Loaded datastore config: {key}")
            except Exception as e:
                if raise_errors:
                    raise
                logger.exception(f"Failed to load datastore config '{key}': {e}")

    def save_datastore_config(self, key: ModbusKey) -> None:
        """Save datastore config to disk.

        Args:
            key: Device key.
        """
        if key not in self._datastore_configs:
            return

        config = self._datastore_configs[key]
        self._datastore_path.write_object(serialize(config), str(key))
        logger.info(f"Saved datastore config: {key}")

    def save_all_datastore_configs(self) -> None:
        """Save all datastore configs to disk."""
        for key in self._datastore_configs:
            self.save_datastore_config(key)

    def _create_datastore_from_config(
        self,
        key: ModbusKey,
    ) -> ModbusDataStore:
        """Create or get a datastore, initializing from config if available."""
        if key in self._data_stores:
            return self._data_stores[key]

        datastore = ModbusDataStore()

        if key in self._datastore_configs:
            config = self._datastore_configs[key]
            for addr, coil_value in config.coils.items():
                datastore.set_coil(addr, coil_value)
            for addr, di_value in config.discrete_inputs.items():
                datastore.set_discrete_inputs(addr, [di_value])
            for addr, hr_value in config.holding_registers.items():
                datastore.set_holding_register(addr, hr_value)
            for addr, ir_value in config.input_registers.items():
                datastore.set_input_registers(addr, [ir_value])

        self._data_stores[key] = datastore
        return datastore

    def update_datastore_config_from_store(self, key: ModbusKey) -> None:
        """Update datastore config from the current datastore state.

        Note: With Dict-based config, this is a no-op since the config
        is directly edited by the user and synced to the datastore.

        Args:
            key: Device key.
        """
        pass

    def add_device(
        self,
        name: str,
        role: ModbusRole,
        host: str = "localhost",
        port: int = 502,
        unit_id: int = 1,
        timeout: float = 5.0,
        reconnect_interval: float = 5.0,
        autostart: bool = False,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[ModbusKey, ModbusDeviceConfig]:
        """Add a new Modbus device.

        Args:
            name: Device name.
            role: Device role (server or client).
            host: Host address.
            port: Port number.
            unit_id: Unit identifier.
            timeout: Timeout in seconds.
            reconnect_interval: Reconnect interval in seconds.
            autostart: Whether to auto-start on load.
            uuid: Optional UUID (generated if not provided).

        Returns:
            Tuple of (key, config).
        """
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        config = ModbusDeviceConfig(
            uuid=uuid,
            name=name,
            role=role,
            host=host,
            port=port,
            unit_id=unit_id,
            timeout=timeout,
            reconnect_interval=reconnect_interval,
            autostart=autostart,
        )
        assert uuid == str(config.key)

        self.add(config.key, config)
        logger.info(f"Added Modbus device: {name} ({role})")

        return config.key, config

    def start_server(
        self,
        key: ModbusKey,
        datastore: Optional[ModbusDataStore] = None,
    ) -> ModbusTcpServer:
        """Start a Modbus TCP server.

        Args:
            key: Device key.
            datastore: Optional datastore (creates new if None).

        Returns:
            The started server.

        Raises:
            KeyError: If device not found.
            ValueError: If device is not a server.
        """
        config = self[key]

        if not config.is_server:
            raise ValueError(f"Device {key} is not configured as a server")

        if key in self._servers:
            server = self._servers[key]
            if server.is_running:
                logger.warning(f"Server {key} is already running")
                return server

        if datastore is None:
            datastore = self._create_datastore_from_config(key)

        server = ModbusTcpServer(
            host=config.host,
            port=config.port,
            datastore=datastore,
            unit_id=config.unit_id,
        )
        server.start()
        self._servers[key] = server

        logger.info(
            f"Started Modbus server: {config.name} on {config.host}:{config.port}"
        )
        return server

    def stop_server(self, key: ModbusKey, *, save_datastore: bool = True) -> None:
        """Stop a Modbus TCP server.

        Args:
            key: Device key.
            save_datastore: Whether to save datastore config before stopping.
        """
        if key not in self._servers:
            logger.warning(f"Server {key} is not running")
            return

        if save_datastore:
            self.update_datastore_config_from_store(key)
            self.save_datastore_config(key)

        server = self._servers.pop(key)
        server.stop()
        logger.info(f"Stopped Modbus server: {key}")

    def connect_client(self, key: ModbusKey) -> ModbusTcpClient:
        """Connect a Modbus TCP client.

        Args:
            key: Device key.

        Returns:
            The connected client.

        Raises:
            KeyError: If device not found.
            ValueError: If device is not a client.
        """
        config = self[key]

        if not config.is_client:
            raise ValueError(f"Device {key} is not configured as a client")

        if key in self._clients:
            client = self._clients[key]
            if client.is_running:
                logger.warning(f"Client {key} is already running")
                return client

        client = ModbusTcpClient(
            host=config.host,
            port=config.port,
            unit_id=config.unit_id,
            timeout=config.timeout,
            reconnect_interval=config.reconnect_interval,
        )
        client.start()
        self._clients[key] = client

        logger.info(
            f"Started Modbus client: {config.name} -> {config.host}:{config.port}"
        )
        return client

    def disconnect_client(self, key: ModbusKey) -> None:
        """Disconnect a Modbus TCP client.

        Args:
            key: Device key.
        """
        if key not in self._clients:
            logger.warning(f"Client {key} is not running")
            return

        client = self._clients.pop(key)
        client.stop()
        logger.info(f"Disconnected Modbus client: {key}")

    def start_autostart_devices(self) -> None:
        """Start all devices configured with autostart=True."""
        for key, config in self.items():
            if config.autostart:
                try:
                    if config.is_server:
                        self.start_server(key)
                    else:
                        self.connect_client(key)
                except Exception as e:
                    logger.error(f"Failed to autostart device {key}: {e}")

    def shutdown_all(self) -> None:
        """Shutdown all running servers and clients."""
        logger.info("Shutting down all Modbus connections...")

        for key in list(self._servers.keys()):
            try:
                self.stop_server(key)
            except Exception as e:
                logger.error(f"Error stopping server {key}: {e}")

        for key in list(self._clients.keys()):
            try:
                self.disconnect_client(key)
            except Exception as e:
                logger.error(f"Error disconnecting client {key}: {e}")

        self._data_stores.clear()
        logger.info("All Modbus connections shut down")

    def remove_device(self, key: ModbusKey) -> None:
        """Remove a device and stop any running connections.

        Args:
            key: Device key.
        """
        if key in self._servers:
            self.stop_server(key, save_datastore=False)

        if key in self._clients:
            self.disconnect_client(key)

        if key in self._data_stores:
            del self._data_stores[key]

        if key in self._datastore_configs:
            del self._datastore_configs[key]
            datastore_file = self._datastore_path.make_object_path(str(key)).as_path()
            if datastore_file.exists():
                datastore_file.unlink()

        self.remove(key)
        logger.info(f"Removed Modbus device: {key}")

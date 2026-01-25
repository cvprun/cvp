# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import Dict, NewType
from uuid import uuid4

ModbusKey = NewType("ModbusKey", str)


@unique
class ModbusRole(StrEnum):
    server = auto()
    client = auto()


@dataclass
class ModbusDeviceConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    role: ModbusRole = ModbusRole.client
    host: str = "localhost"
    port: int = 502
    unit_id: int = 1
    timeout: float = 5.0
    reconnect_interval: float = 5.0
    autostart: bool = False

    @property
    def key(self) -> ModbusKey:
        return ModbusKey(self.uuid)

    @key.setter
    def key(self, value: ModbusKey) -> None:
        self.uuid = str(value)

    @property
    def is_server(self) -> bool:
        return self.role == ModbusRole.server

    @property
    def is_client(self) -> bool:
        return self.role == ModbusRole.client


@dataclass
class ModbusDataStoreConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    coils: Dict[int, bool] = field(default_factory=dict)
    discrete_inputs: Dict[int, bool] = field(default_factory=dict)
    holding_registers: Dict[int, int] = field(default_factory=dict)
    input_registers: Dict[int, int] = field(default_factory=dict)

    @property
    def key(self) -> ModbusKey:
        return ModbusKey(self.uuid)

    @key.setter
    def key(self, value: ModbusKey) -> None:
        self.uuid = str(value)

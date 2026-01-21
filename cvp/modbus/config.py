# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import NewType
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

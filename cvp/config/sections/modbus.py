# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ModbusConfig:
    host: str = "localhost"
    port: int = 502
    autostart: bool = False
    server_unit_id: int = 1
    timeout: float = 5.0
    reconnect_interval: float = 5.0

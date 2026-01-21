# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class HubConfig:
    host: str = "localhost"
    port: int = 9090
    autostart: bool = True

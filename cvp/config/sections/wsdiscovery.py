# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.variables import (
    WSD_MULTICAST_UDP_REPEAT,
    WSD_PORT_NUMBER,
    WSD_RELATES_TO,
    WSD_TIMEOUT,
    WSD_UNICAST_ADDRESS,
    WSD_UNICAST_UDP_REPEAT,
)


@unique
class CastType(StrEnum):
    multicast = auto()
    unicast = auto()


@dataclass
class WsDiscoveryConfig:
    selected: str = field(default_factory=str)
    cast_type: CastType = CastType.multicast
    address: str = WSD_UNICAST_ADDRESS
    port: int = WSD_PORT_NUMBER
    timeout: float = WSD_TIMEOUT
    multicast_repeat: int = WSD_MULTICAST_UDP_REPEAT
    unicast_repeat: int = WSD_UNICAST_UDP_REPEAT
    relates_to: bool = WSD_RELATES_TO

    def reset_defaults(self):
        self.cast_type = CastType.multicast
        self.address = WSD_UNICAST_ADDRESS
        self.port = WSD_PORT_NUMBER
        self.timeout = WSD_TIMEOUT
        self.multicast_repeat = WSD_MULTICAST_UDP_REPEAT
        self.unicast_repeat = WSD_UNICAST_UDP_REPEAT
        self.relates_to = WSD_RELATES_TO

    @property
    def is_unicast(self) -> bool:
        return self.cast_type == CastType.unicast

    @property
    def is_multicast(self) -> bool:
        return self.cast_type == CastType.multicast

    def set_unicast(self) -> None:
        self.cast_type = CastType.unicast

    def set_multicast(self) -> None:
        self.cast_type = CastType.multicast

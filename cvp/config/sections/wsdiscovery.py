# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.variables import (
    WSD_IPV4_MULTICAST_ADDRESS,
    WSD_IPV6_MULTICAST_ADDRESS,
    WSD_PORT_NUMBER,
    WSD_TIMEOUT,
)


@unique
class WsdProtocol(StrEnum):
    tcp = auto()
    udp = auto()


@dataclass
class WsDiscoveryConfig:
    protocol: WsdProtocol = WsdProtocol.udp
    ipv4_address: str = WSD_IPV4_MULTICAST_ADDRESS
    ipv6_address: str = WSD_IPV6_MULTICAST_ADDRESS
    port: int = WSD_PORT_NUMBER
    timeout: float = WSD_TIMEOUT
    selected: str = field(default_factory=str)

    def reset_defaults(self):
        self.protocol = WsdProtocol.udp
        self.ipv4_address = WSD_IPV4_MULTICAST_ADDRESS
        self.ipv6_address = WSD_IPV6_MULTICAST_ADDRESS
        self.port = WSD_PORT_NUMBER
        self.timeout = WSD_TIMEOUT

    @property
    def is_tcp(self) -> bool:
        return self.protocol == WsdProtocol.tcp

    @property
    def is_udp(self) -> bool:
        return self.protocol == WsdProtocol.udp

    def set_tcp(self) -> None:
        self.protocol = WsdProtocol.tcp

    def set_udp(self) -> None:
        self.protocol = WsdProtocol.udp

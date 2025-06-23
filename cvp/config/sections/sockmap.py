# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.network.address_range import calc_ip_range
from cvp.strings.parse_number_ranges import parse_integer_ranges
from cvp.variables import (
    SOCKMAP_ADDRESS_BEGIN,
    SOCKMAP_ADDRESS_END,
    SOCKMAP_PORT_RANGE,
    SOCKMAP_TIMEOUT,
)


@dataclass
class SockmapConfig:
    address_begin: str = SOCKMAP_ADDRESS_BEGIN
    address_end: str = SOCKMAP_ADDRESS_END
    port_range: str = SOCKMAP_PORT_RANGE
    timeout: float = SOCKMAP_TIMEOUT

    def reset_defaults(self):
        self.address_begin = SOCKMAP_ADDRESS_BEGIN
        self.address_end = SOCKMAP_ADDRESS_END
        self.port_range = SOCKMAP_PORT_RANGE
        self.timeout = SOCKMAP_TIMEOUT

    def as_list(self):
        result = list()
        for ip in sorted(calc_ip_range(self.address_begin, self.address_end)):
            for port in sorted(parse_integer_ranges(self.port_range)):
                result.append((ip, port))
        return result

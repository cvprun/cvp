# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Connection:
    """SDP connection (c=).

    Format: c=<nettype> <addrtype> <connection-address>
    """

    nettype: str
    addrtype: str
    connection_address: str

    def encode(self) -> str:
        return f"c={self.nettype} {self.addrtype} {self.connection_address}"

    @classmethod
    def parse(cls, line: str) -> "Connection":
        if not line.startswith("c="):
            raise ValueError(f"Invalid connection line: {line}")
        content = line[2:]
        parts = content.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid connection format: {line}")
        return cls(
            nettype=parts[0],
            addrtype=parts[1],
            connection_address=parts[2],
        )

    def __str__(self) -> str:
        return self.encode()

# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Origin:
    """SDP origin (o=).

    Format: o=<username> <sess-id> <sess-version> <nettype> <addrtype> <unicast-address>
    """

    username: str
    sess_id: str
    sess_version: int
    nettype: str
    addrtype: str
    unicast_address: str

    def encode(self) -> str:
        return (
            f"o={self.username} {self.sess_id} {self.sess_version} "
            f"{self.nettype} {self.addrtype} {self.unicast_address}"
        )

    @classmethod
    def parse(cls, line: str) -> "Origin":
        if not line.startswith("o="):
            raise ValueError(f"Invalid origin line: {line}")
        content = line[2:]
        parts = content.split()
        if len(parts) != 6:
            raise ValueError(f"Invalid origin format: {line}")
        return cls(
            username=parts[0],
            sess_id=parts[1],
            sess_version=int(parts[2]),
            nettype=parts[3],
            addrtype=parts[4],
            unicast_address=parts[5],
        )

    def __str__(self) -> str:
        return self.encode()

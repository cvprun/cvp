# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Bandwidth:
    """SDP bandwidth (b=).

    Format: b=<bwtype>:<bandwidth>
    """

    bwtype: str
    bandwidth: int

    def encode(self) -> str:
        return f"b={self.bwtype}:{self.bandwidth}"

    @classmethod
    def parse(cls, line: str) -> "Bandwidth":
        if not line.startswith("b="):
            raise ValueError(f"Invalid bandwidth line: {line}")
        content = line[2:]
        if ":" not in content:
            raise ValueError(f"Invalid bandwidth format: {line}")
        bwtype, bandwidth = content.split(":", 1)
        return cls(bwtype=bwtype, bandwidth=int(bandwidth))

    def __str__(self) -> str:
        return self.encode()

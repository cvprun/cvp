# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Timing:
    """SDP timing (t=).

    Format: t=<start-time> <stop-time>
    """

    start_time: int
    stop_time: int

    def encode(self) -> str:
        return f"t={self.start_time} {self.stop_time}"

    @classmethod
    def parse(cls, line: str) -> "Timing":
        if not line.startswith("t="):
            raise ValueError(f"Invalid timing line: {line}")
        content = line[2:]
        parts = content.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid timing format: {line}")
        return cls(start_time=int(parts[0]), stop_time=int(parts[1]))

    def __str__(self) -> str:
        return self.encode()

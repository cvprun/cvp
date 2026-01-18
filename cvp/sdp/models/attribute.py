# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class Attribute:
    """SDP attribute (a=).

    Format: a=<name> or a=<name>:<value>
    """

    name: str
    value: Optional[str] = None

    def encode(self) -> str:
        if self.value is not None:
            return f"a={self.name}:{self.value}"
        return f"a={self.name}"

    @classmethod
    def parse(cls, line: str) -> "Attribute":
        if not line.startswith("a="):
            raise ValueError(f"Invalid attribute line: {line}")
        content = line[2:]
        if ":" in content:
            name, value = content.split(":", 1)
            return cls(name=name, value=value)
        return cls(name=content)

    def __str__(self) -> str:
        return self.encode()

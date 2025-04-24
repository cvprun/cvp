# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class FlowWorkspace:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)

    def open(self) -> bool:
        return False

    def close(self):
        pass

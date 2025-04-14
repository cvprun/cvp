# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List


@dataclass
class WsDiscovery:
    epr: str = field(default_factory=str)  # EndPoint Reference
    instance_id: int = -1
    message_number: int = -1
    metadata_version: int = -1
    scopes: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)
    xaddrs: List[str] = field(default_factory=list)
    name: str = field(default_factory=str)
    error: str = field(default_factory=str)

    @property
    def has_error(self) -> bool:
        return bool(self.error)

    @property
    def has_onvif_scope(self) -> bool:
        if not self.scopes:
            return False
        for scope in self.scopes:
            if scope.startswith("onvif://"):
                return True
        return False

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, NewType

from cvp.variables import (
    WSD_INVALID_INSTANCE_ID,
    WSD_INVALID_MESSAGE_NUMBER,
    WSD_INVALID_METADATA_VERSION,
)

EprKey = NewType("EprKey", str)


@dataclass
class WsDiscovery:
    epr: EprKey = field(default_factory=lambda: EprKey(str()))  # EndPoint Reference
    instance_id: int = WSD_INVALID_INSTANCE_ID
    message_number: int = WSD_INVALID_MESSAGE_NUMBER
    metadata_version: int = WSD_INVALID_METADATA_VERSION
    scopes: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)
    xaddrs: List[str] = field(default_factory=list)
    name: str = field(default_factory=str)
    error: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

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

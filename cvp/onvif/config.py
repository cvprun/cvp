# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import NewType, Optional
from uuid import uuid4

OnvifKey = NewType("OnvifKey", str)


@unique
class HttpAuth(StrEnum):
    basic = auto()
    digest = auto()


@dataclass
class OnvifConfig:
    key: OnvifKey = field(default_factory=lambda: OnvifKey(str(uuid4())))
    name: str = field(default_factory=str)
    address: str = field(default_factory=str)
    username: str = field(default_factory=str)

    http_auth: Optional[HttpAuth] = None
    use_wsse: bool = False
    encode_digest: bool = False
    no_verify: bool = False
    no_file_cache: bool = False
    same_host: bool = False

    # GUI Handling
    select_binding: str = field(default_factory=str)
    select_api: str = field(default_factory=str)

    @property
    def is_http_basic(self):
        return self.http_auth == HttpAuth.basic

    @property
    def is_http_digest(self):
        return self.http_auth == HttpAuth.digest

    def set_http_basic(self) -> None:
        self.http_auth = HttpAuth.basic

    def set_http_digest(self) -> None:
        self.http_auth = HttpAuth.digest

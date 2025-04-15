# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import Optional
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.palette.basic import GREEN, RED, YELLOW
from cvp.types.colors import RGBA
from cvp.variables import API_SELECT_WIDTH, MAX_API_SELECT_WIDTH, MIN_API_SELECT_WIDTH


@unique
class HttpAuth(StrEnum):
    basic = auto()
    digest = auto()


@dataclass
class OnvifConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    address: str = field(default_factory=str)
    use_wsse: bool = False
    username: str = field(default_factory=str)
    # 'password' is stored in the keyring.
    encode_digest: bool = False
    http_auth: Optional[HttpAuth] = None
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


@dataclass
class OnvifManagerConfig(ManagerWindowConfig):
    preload: bool = False

    api_select_width: float = API_SELECT_WIDTH
    min_api_select_width: float = MIN_API_SELECT_WIDTH
    max_api_select_width: float = MAX_API_SELECT_WIDTH

    success_color: RGBA = field(default_factory=lambda: (*GREEN, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    typename_color: RGBA = field(default_factory=lambda: (1.0, 0.647, 0.0, 1.0))

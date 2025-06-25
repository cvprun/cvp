# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Union


@dataclass
class HttpxInitialParams:
    auth_type: str = field(default_factory=str)
    auth_params: List[str] = field(default_factory=list)
    query_params: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    verify: bool = True
    trust_env: bool = True
    http1: bool = True
    http2: bool = False
    proxy: str = field(default_factory=str)
    timeout: float = 5.0
    follow_redirects: bool = False
    max_connections: int = 100
    max_keepalive_connections: int = 20
    max_redirects: int = 20
    base_url: str = field(default_factory=str)
    default_encoding: str = "utf-8"

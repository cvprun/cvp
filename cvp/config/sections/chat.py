# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class ChatConfig:
    selected_server_key: str = field(default_factory=str)
    selected_model_name: str = field(default_factory=str)

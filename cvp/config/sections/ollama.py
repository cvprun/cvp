# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class OllamaConfig:
    selected: str = field(default_factory=str)

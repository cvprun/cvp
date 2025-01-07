# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.config.sections.bases.window import WindowConfig


@dataclass
class HexWindowConfig(WindowConfig):
    file: str = field(default_factory=str)


@dataclass
class HexManagerConfig(ManagerWindowConfig):
    pass

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.config.sections.bases.window import WindowConfig


@dataclass
class HexWindowConfig(WindowConfig):
    history: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)

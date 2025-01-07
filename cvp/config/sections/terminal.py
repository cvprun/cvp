# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.config.sections.bases.window import WindowConfig


@dataclass
class TerminalWindowConfig(WindowConfig):
    tty: List[str] = field(default_factory=list)

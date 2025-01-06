# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.window import WindowConfig


@dataclass
class TextWindowConfig(WindowConfig):
    file: str = field(default_factory=str)

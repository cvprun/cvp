# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class PreferenceManagerConfig(ManagerWindowConfig):
    selected_submenus: Dict[str, str] = field(default_factory=dict)
    selected_menu: str = field(default_factory=str)

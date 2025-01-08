# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import uuid4

from cvp.config.sections.bases.manager import ManagerWindowConfig


@dataclass
class WorkerManagerConfig(ManagerWindowConfig):
    pass


@dataclass
class WorkerConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)

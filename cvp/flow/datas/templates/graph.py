# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from cvp.flow.datas.templates.node import NodeTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


@dataclass
class GraphTemplate:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()
    icon: str = str()
    color: RGBA = WHITE_RGBA
    nodes: List[NodeTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

# -*- coding: utf-8 -*-

from typing import List, Optional

from cvp.templates.node import NodeTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


class GraphTemplate:
    def __init__(
        self,
        name: str,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        nodes: Optional[List[NodeTemplate]] = None,
        tags: Optional[List[str]] = None,
    ):
        self.name = name
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.color = color if color else WHITE_RGBA
        self.nodes = list(nodes if nodes else [])
        self.tags = list(tags if tags else [])

# -*- coding: utf-8 -*-

from typing import Optional

from cvp.types.colors import RGBA, WHITE_RGBA


class Dtype:
    def __init__(
        self,
        name: str,
        path: str,
        base: type,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        self.name = name
        self.path = path
        self.base = base
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.color = color if color else WHITE_RGBA

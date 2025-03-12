# -*- coding: utf-8 -*-

from typing import Optional


class WireKey(str):
    pass


class WireTemplate:
    def __init__(self, key: WireKey, docs: Optional[str] = None):
        self.key = key
        self.docs = docs if docs else str()

# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNode


class FloatingNode(CastingNode):
    def __init__(self):
        super().__init__(float)

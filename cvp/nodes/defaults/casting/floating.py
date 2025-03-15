# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNodeTemplate


class FloatingNodeTemplate(CastingNodeTemplate):
    def __init__(self):
        super().__init__(float)

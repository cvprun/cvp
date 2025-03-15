# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNodeTemplate


class StringNodeTemplate(CastingNodeTemplate):
    def __init__(self):
        super().__init__(str)

# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNode


class FloatingCasting(CastingNode):
    """Casting to float type"""

    def __init__(self):
        super().__init__(float)

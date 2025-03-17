# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNode


class IntegerCasting(CastingNode):
    """Casting to int type"""

    def __init__(self):
        super().__init__(int)

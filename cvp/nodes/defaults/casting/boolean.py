# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNode


class BooleanCasting(CastingNode):
    """Casting to bool type"""

    def __init__(self):
        super().__init__(bool)

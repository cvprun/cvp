# -*- coding: utf-8 -*-

from cvp.nodes.defaults.casting._base import CastingNode


class StringCasting(CastingNode):
    """Casting to str type"""

    def __init__(self):
        super().__init__(str)

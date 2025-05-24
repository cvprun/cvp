# -*- coding: utf-8 -*-

from enum import Enum

from cvp.imgui.combo import INFINITY_HEIGHT_IN_ITEMS
from cvp.imgui.combo import combo as _combo


def combo_enum(
    label: str,
    current: Enum,
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    enums = list(type(current))
    index = enums.index(current)
    items = [(e if isinstance(e, str) else e.name) for e in enums]
    return _combo(label, index, items, height_in_items)

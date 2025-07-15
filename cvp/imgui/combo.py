# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence

from imgui_bundle import imgui

from cvp.imgui.calc_combo_size import calc_max_combo_size
from cvp.variables import INFINITY_HEIGHT_IN_ITEMS


class ComboResult(NamedTuple):
    changed: bool
    value: int  # NamedTuple already has an 'index' symbol, so replace it with 'value'.
    item: Optional[str]

    @classmethod
    def from_raw(cls, result, *, items: Optional[Sequence[str]] = None):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        item = items[value] if items and 0 <= value < len(items) else None
        return cls(changed, value, item)

    def __bool__(self) -> bool:
        return self.changed


def combo(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    if not isinstance(items, list):
        items = list(items)
    result = imgui.combo(label, current, items, height_in_items)
    return ComboResult.from_raw(result, items=items)


def combo_fitting_items_max_width(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    imgui.set_next_item_width(calc_max_combo_size(label, items).x)
    return combo(label, current, items, height_in_items)

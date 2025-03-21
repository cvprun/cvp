# -*- coding: utf-8 -*-

from typing import NamedTuple, Sequence

from imgui_bundle import imgui


class ComboResult(NamedTuple):
    changed: bool
    value: int  # NamedTuple already has an 'index' symbol, so replace it with 'value'.

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        return cls(changed, value)

    def __bool__(self) -> bool:
        return self.changed


def combo(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=-1,
):
    if not isinstance(items, list):
        items = list(items)
    result = imgui.combo(label, current, items, height_in_items)
    return ComboResult.from_raw(result)

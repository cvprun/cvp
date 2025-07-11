# -*- coding: utf-8 -*-

from typing import NamedTuple, Union
from zoneinfo import ZoneInfo

from cvp.chrono.timezones import ZONE_NAMES
from cvp.imgui.combo import INFINITY_HEIGHT_IN_ITEMS
from cvp.imgui.combo import combo as _combo


class ComboTimezoneResult(NamedTuple):
    changed: bool
    value: int  # NamedTuple already has an 'index' symbol, so replace it with 'value'.
    tzname: str

    def as_timezone(self) -> ZoneInfo:
        return ZoneInfo(self.tzname)


def combo_timezone(
    label: str,
    current: Union[int, str, ZoneInfo],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    if isinstance(current, ZoneInfo):
        index = ZONE_NAMES.index(current.key)
    elif isinstance(current, str):
        index = ZONE_NAMES.index(current)
    elif isinstance(current, int):
        index = current
    else:
        raise TypeError(f"Unsupported current type: {type(current).__name__}")

    result = _combo(label, index, ZONE_NAMES, height_in_items)
    assert isinstance(result.item, str)
    return ComboTimezoneResult(result.changed, result.value, result.item)

# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union
from zoneinfo import ZoneInfo

from cvp.chrono.timezones import UTC_OFFSETS, ZONE_NAMES
from cvp.imgui.combo_with_filter import combo_with_filter
from cvp.imgui.flags.combo import ComboFlags
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.variables import LABEL_FILTER


class ComboTimezoneResult(NamedTuple):
    changed: bool
    value: int  # NamedTuple already has an 'index' symbol, so replace it with 'value'.
    tzname: str
    filter_changed: bool
    filter_value: Optional[str]

    def __bool__(self) -> bool:
        return self.changed or self.filter_changed

    def as_timezone(self) -> ZoneInfo:
        return ZoneInfo(self.tzname)


def combo_timezone(
    label: str,
    current: Union[int, str, ZoneInfo],
    height_in_items: Optional[int] = None,
    flags: Union[ComboFlags, int] = 0,
    filter_value: Optional[str] = None,
    filter_flags: Union[InputTextFlags, int] = 0,
    filter_hint=LABEL_FILTER,
):
    if isinstance(current, ZoneInfo):
        index = ZONE_NAMES.index(current.key)
    elif isinstance(current, str):
        index = ZONE_NAMES.index(current)
    elif isinstance(current, int):
        index = current
    else:
        raise TypeError(f"Unsupported current type: {type(current).__name__}")

    result = combo_with_filter(
        label=label,
        current=index,
        items=ZONE_NAMES,
        height_in_items=height_in_items,
        flags=flags,
        filter_value=filter_value,
        filter_flags=filter_flags,
        filter_hint=filter_hint,
        filter_ignore_case=True,
        extra_hints=UTC_OFFSETS,
    )

    return ComboTimezoneResult(
        result.changed,
        result.value,
        result.item,
        result.filter_changed,
        result.filter_value,
    )

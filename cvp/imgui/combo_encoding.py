# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union

from cvp.encoding.lookup import TEXT_ENCODINGS
from cvp.imgui.combo_with_filter import combo_with_filter
from cvp.imgui.flags.combo import ComboFlags
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.variables import LABEL_FILTER


class ComboEncodingResult(NamedTuple):
    changed: bool
    value: int  # NamedTuple already has an 'index' symbol, so replace it with 'value'.
    encoding: str
    filter_changed: bool
    filter_value: Optional[str]

    def __bool__(self) -> bool:
        return self.changed or self.filter_changed


def combo_text_encoding(
    label: str,
    value: Union[str, int],
    height_in_items: Optional[int] = None,
    flags: Union[ComboFlags, int] = 0,
    filter_value: Optional[str] = None,
    filter_flags: Union[InputTextFlags, int] = 0,
    filter_hint=LABEL_FILTER,
):
    if isinstance(value, str):
        item_index = TEXT_ENCODINGS.index(value)
    elif isinstance(value, int):
        item_index = value
    else:
        raise TypeError(f"Unsupported value type: {type(value).__name__}")

    result = combo_with_filter(
        label=label,
        value=item_index,
        items=TEXT_ENCODINGS,
        height_in_items=height_in_items,
        flags=flags,
        filter_value=filter_value,
        filter_flags=filter_flags,
        filter_hint=filter_hint,
        filter_ignore_case=True,
    )

    return ComboEncodingResult(
        result.changed,
        result.value,
        result.item,
        result.filter_changed,
        result.filter_value,
    )

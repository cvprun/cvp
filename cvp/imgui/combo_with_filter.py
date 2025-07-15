# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.imgui.flags.combo import ComboFlags
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.variables import INFINITY_HEIGHT_IN_ITEMS, LABEL_FILTER, NOT_FOUND_INDEX


class ComboWithFilterResult(NamedTuple):
    changed: bool
    value: int
    item: Optional[str]
    filter_changed: bool
    filter_value: Optional[str]


def combo_with_filter(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
    flags: Union[ComboFlags, int] = 0,
    filter_value: Optional[str] = None,
    filter_flags: Union[InputTextFlags, int] = 0,
    filter_hint=LABEL_FILTER,
    *,
    not_found_item_name: Optional[str] = None,
):
    if not isinstance(items, list):
        items = list(items)
    if isinstance(flags, ComboFlags):
        flags = int(flags)
    assert isinstance(items, list)
    assert isinstance(flags, int)

    if 0 <= current < len(items):
        preview_value = items[current]
    else:
        preview_value = not_found_item_name if not_found_item_name else str()

    filter_changed = False
    selected_index = NOT_FOUND_INDEX

    if imgui.begin_combo(label, preview_value, flags):
        try:
            if filter_value is not None:
                filter_result = imgui.input_text_with_hint(
                    "##Filter",
                    filter_hint,
                    filter_value,
                    filter_flags,
                )
                filter_changed = filter_result[0]
                if filter_changed:
                    filter_value = filter_result[1]

            for i, item in enumerate(items):
                if 0 <= height_in_items <= i:
                    break

                assert isinstance(item, str)
                if filter_value and item.find(filter_value) == NOT_FOUND_INDEX:
                    break

                is_selected = current == i
                if imgui.selectable(item, is_selected)[0]:
                    assert selected_index == NOT_FOUND_INDEX
                    selected_index = i

                # Set the initial focus when opening the combo
                # (scrolling + keyboard navigation focus)
                if is_selected:
                    imgui.set_item_default_focus()
        finally:
            imgui.end_combo()

    return ComboWithFilterResult(
        changed=selected_index != NOT_FOUND_INDEX,
        value=selected_index,
        item=items[selected_index] if selected_index != NOT_FOUND_INDEX else None,
        filter_changed=filter_changed,
        filter_value=filter_value,
    )

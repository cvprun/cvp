# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.combo import ComboFlags
from cvp.imgui.flags.input_text import InputTextFlags
from cvp.variables import INFINITY_HEIGHT_IN_ITEMS, LABEL_FILTER, NOT_FOUND_INDEX


class ComboWithFilterResult(NamedTuple):
    changed: bool
    value: int
    item: Optional[str]
    filter_changed: bool
    filter_value: Optional[str]

    def __bool__(self) -> bool:
        return self.changed or self.filter_changed


def combo_with_filter(
    label: str,
    value: int,
    items: Sequence[str],
    height_in_items: Optional[int] = None,
    flags: Union[ComboFlags, int] = 0,
    filter_value: Optional[str] = None,
    filter_flags: Union[InputTextFlags, int] = 0,
    filter_hint=LABEL_FILTER,
    filter_ignore_case=False,
    *,
    not_found_item_name: Optional[str] = None,
    extra_hints: Optional[Sequence[str]] = None,
):
    if isinstance(flags, ComboFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if 0 <= value < len(items):
        preview_value = items[value]
    else:
        preview_value = not_found_item_name if not_found_item_name else str()

    initial_value = value
    filter_changed = False

    # Set the combo popup height according to height_in_items
    if height_in_items is not None:
        if height_in_items == INFINITY_HEIGHT_IN_ITEMS:
            height_in_items = len(items)

        items_height = imgui.get_text_line_height_with_spacing() * height_in_items
        padding_height = imgui.get_style().window_padding.y * 2
        popup_max_height = items_height + padding_height
        imgui.set_next_window_size_constraints(
            size_min=(0, 0),
            size_max=(imgui.FLT_MAX, popup_max_height),
        )

    if imgui.begin_combo(label, preview_value, flags):
        try:
            if filter_value is not None:
                if isinstance(filter_flags, InputTextFlags):
                    filter_flags = int(filter_flags)
                assert isinstance(filter_flags, int)

                imgui.set_next_item_width(FIT_WIDTH)
                filter_changed, filter_value = imgui.input_text_with_hint(
                    "##Filter",
                    filter_hint,
                    filter_value,
                    filter_flags,
                )

            if filter_value and filter_ignore_case:
                filter_key = filter_value.lower()
            else:
                filter_key = filter_value or str()

            for i, item in enumerate(items):
                assert isinstance(item, str)

                if filter_key:
                    item_key = item.lower() if filter_ignore_case else item
                    if item_key.find(filter_key) == NOT_FOUND_INDEX:
                        continue

                selected = value == i
                if imgui.selectable(item, selected)[0]:
                    value = i

                if extra_hints and 0 <= i < len(extra_hints):
                    imgui.same_line()
                    imgui.text_disabled(extra_hints[i])

                # Set the initial focus when opening the combo
                # (scrolling + keyboard navigation focus)
                if selected:
                    imgui.set_item_default_focus()

            min_item_index = 0
            max_item_index = len(items) - 1

            if imgui.is_key_pressed(imgui.Key.home, repeat=False):
                value = min_item_index
            if imgui.is_key_pressed(imgui.Key.up_arrow, repeat=True):
                value = max(min_item_index, value - 1)
            if imgui.is_key_pressed(imgui.Key.down_arrow, repeat=True):
                value = min(max_item_index, value + 1)
            if imgui.is_key_pressed(imgui.Key.end, repeat=False):
                value = max_item_index
        finally:
            imgui.end_combo()

    return ComboWithFilterResult(
        changed=value != initial_value,
        value=value,
        item=items[value] if 0 <= value < len(items) else None,
        filter_changed=filter_changed,
        filter_value=filter_value,
    )

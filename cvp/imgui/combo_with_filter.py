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
    current: int,
    items: Sequence[str],
    height_in_items: Optional[int] = None,
    flags: Union[ComboFlags, int] = 0,
    filter_value: Optional[str] = None,
    filter_flags: Union[InputTextFlags, int] = 0,
    filter_hint=LABEL_FILTER,
    filter_ignore_case=False,
    *,
    not_found_item_name: Optional[str] = None,
):
    if isinstance(flags, ComboFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if 0 <= current < len(items):
        preview_value = items[current]
    else:
        preview_value = not_found_item_name if not_found_item_name else str()

    changed = False
    filter_changed = False
    filter_key = filter_value

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
                imgui.set_next_item_width(FIT_WIDTH)
                filter_result = imgui.input_text_with_hint(
                    "##Filter",
                    filter_hint,
                    filter_value,
                    filter_flags,
                )
                filter_changed = filter_result[0]
                filter_value = filter_result[1]

                if filter_ignore_case:
                    filter_key = filter_value.lower()
                else:
                    filter_key = filter_value

            for i, item in enumerate(items):
                assert isinstance(item, str)

                if filter_key:
                    item_key = item.lower() if filter_ignore_case else item
                    if item_key.find(filter_key) == NOT_FOUND_INDEX:
                        continue

                is_selected = current == i
                if imgui.selectable(item, is_selected)[0]:
                    changed = True
                    current = i

                # Set the initial focus when opening the combo
                # (scrolling + keyboard navigation focus)
                if is_selected:
                    imgui.set_item_default_focus()
        finally:
            imgui.end_combo()

    return ComboWithFilterResult(
        changed=changed,
        value=current,
        item=items[current] if 0 <= current < len(items) else None,
        filter_changed=filter_changed,
        filter_value=filter_value,
    )

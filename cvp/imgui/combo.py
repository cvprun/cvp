# -*- coding: utf-8 -*-

from typing import Final, NamedTuple, Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.imgui.flags.combo import NO_ARROW_BUTTON, NO_PREVIEW, ComboFlags
from cvp.variables import NOT_FOUND_INDEX

INFINITY_HEIGHT_IN_ITEMS: Final[int] = -1


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
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    if not isinstance(items, list):
        items = list(items)
    result = imgui.combo(label, current, items, height_in_items)
    return ComboResult.from_raw(result)


def get_arrow_size(flags: Union[ComboFlags, int] = 0) -> float:
    return 0.0 if flags & NO_ARROW_BUTTON else imgui.get_frame_height()


def calc_max_combo_size(
    label: str,
    items: Sequence[str],
    flags: Union[ComboFlags, int] = 0,
) -> imgui.ImVec2:
    label_size = imgui.calc_text_size(label, None, True)
    items_max_width = max((imgui.calc_text_size(i, None, True).x for i in items))
    arrow_size = get_arrow_size(flags)

    frame_padding = imgui.get_style().frame_padding
    padding_x = 0.0 if flags & NO_PREVIEW else frame_padding.x * 2
    padding_y = frame_padding.y * 2

    width = arrow_size + items_max_width + padding_x
    height = label_size.y + padding_y

    return imgui.ImVec2(width, height)


def combo_fitting_items_max_width(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
):
    imgui.set_next_item_width(calc_max_combo_size(label, items).x)
    return combo(label, current, items, height_in_items)


def combo_with_flags(
    label: str,
    current: int,
    items: Sequence[str],
    height_in_items=INFINITY_HEIGHT_IN_ITEMS,
    flags: Union[ComboFlags, int] = 0,
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

    selected_index: Optional[int] = None

    if imgui.begin_combo(label, preview_value, flags):
        try:
            for i, model_name in enumerate(items):
                if 0 <= height_in_items <= i:
                    break

                is_selected = current == i
                if imgui.selectable(model_name, is_selected)[0]:
                    assert selected_index is None
                    selected_index = i

                # Set the initial focus when opening the combo
                # (scrolling + keyboard navigation focus)
                if is_selected:
                    imgui.set_item_default_focus()
        finally:
            imgui.end_combo()

    if selected_index is not None:
        return ComboResult(changed=True, value=selected_index)
    else:
        return ComboResult(changed=False, value=NOT_FOUND_INDEX)

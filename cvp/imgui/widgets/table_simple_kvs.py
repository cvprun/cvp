# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Final, MutableSequence, Optional, Tuple, Union

from imgui_bundle import imgui

from cvp.assets.fonts.mdi import ARROW_DOWN, ARROW_UP, DELETE, PLUS
from cvp.imgui.begin_group import begin_group_context
from cvp.imgui.button import button
from cvp.imgui.calc_button_size import calc_button_size
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags import table_column
from cvp.imgui.flags.style_var import ITEM_SPACING
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS, TableFlags
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.variables import NOT_FOUND_INDEX

DEFAULT_NEW_ELEMENT: Final[Tuple[str, str]] = str(), str()


def table_simple_kvs(
    label: str,
    container: MutableSequence[Tuple[str, str]],
    flags: Union[TableFlags, int] = DEFAULT_TABLE_FLAGS,
    outer_size: Optional[imgui.ImVec2Like] = None,
    inner_width: float = 0.0,
    swappable=False,
    removable=False,
    insertable=False,
    action_button_spacing=1.0,
    new_element=DEFAULT_NEW_ELEMENT,
) -> None:
    if isinstance(flags, TableFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if imgui.begin_table(label, 4, flags, outer_size, inner_width):
        try:
            actions_width = 0.0
            # [Note] When calculating the width, do not include `cell_padding`.
            actions_width += calc_button_size(ARROW_UP).x
            actions_width += action_button_spacing
            actions_width += calc_button_size(ARROW_DOWN).x
            actions_width += action_button_spacing
            actions_width += calc_button_size(PLUS).x
            actions_width += action_button_spacing
            actions_width += calc_button_size(DELETE).x

            imgui.table_setup_column("Index", table_column.WIDTH_FIXED)
            imgui.table_setup_column("Key", table_column.WIDTH_STRETCH)
            imgui.table_setup_column("Value", table_column.WIDTH_STRETCH)
            imgui.table_setup_column("Actions", table_column.WIDTH_FIXED, actions_width)
            imgui.table_headers_row()

            remove_index = NOT_FOUND_INDEX
            insert_index = NOT_FOUND_INDEX
            swap_tuple: Optional[Tuple[int, int]] = None
            last_index = len(container) - 1

            for i, item in enumerate(container):
                key, value = item
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(str(i))

                imgui.table_set_column_index(1)
                imgui.set_next_item_width(FIT_WIDTH)
                key_result = imgui.input_text(f"###HeaderKey{i}", key)
                if key_result[0]:
                    container[i] = key_result[1], value

                imgui.table_set_column_index(2)
                imgui.set_next_item_width(FIT_WIDTH)
                val_result = imgui.input_text(f"###HeaderValue{i}", value)
                if val_result[0]:
                    container[i] = key, val_result[1]

                imgui.table_set_column_index(3)

                with begin_group_context():
                    no_up = not swappable or i == 0
                    no_down = not swappable or i == last_index
                    no_insert = not insertable
                    no_remove = not removable

                    imgui.push_style_var_x(ITEM_SPACING, action_button_spacing)
                    try:
                        if button(f"{ARROW_UP}###Up.{i}", disabled=no_up):
                            swap_tuple = i - 1, i
                        hovered_tooltip_text("Swap with the item above")

                        imgui.same_line()
                        if button(f"{ARROW_DOWN}###Down.{i}", disabled=no_down):
                            swap_tuple = i, i + 1
                        hovered_tooltip_text("Swap with the item below")

                        imgui.same_line()
                        if button(f"{PLUS}##Insert.{i}", disabled=no_insert):
                            insert_index = i
                        hovered_tooltip_text(f"Insert a new item at position {i}")

                        imgui.same_line()
                        if button(f"{DELETE}###Del.{i}", disabled=no_remove):
                            remove_index = i
                        hovered_tooltip_text(f"Delete the item at position {i}")
                    finally:
                        imgui.pop_style_var()

            if insert_index != NOT_FOUND_INDEX:
                container.insert(insert_index, deepcopy(new_element))

            if swap_tuple is not None:
                left, right = swap_tuple
                temp = container[left]
                container[left] = container[right]
                container[right] = temp

            if remove_index != NOT_FOUND_INDEX:
                container.pop(remove_index)
        finally:
            imgui.end_table()

        if insertable:
            if imgui.button(f"{PLUS}##AppendNewItem"):
                container.append(deepcopy(new_element))
            hovered_tooltip_text("Append a new item to the end of the list")

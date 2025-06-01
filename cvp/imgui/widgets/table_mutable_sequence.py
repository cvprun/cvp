# -*- coding: utf-8 -*-

from typing import Any, Callable, MutableSequence, Optional, Tuple, TypeVar, Union

from imgui_bundle import imgui

from cvp.assets.fonts.mdi import ARROW_DOWN, ARROW_UP, DELETE, PLUS
from cvp.imgui.begin_group import begin_group_context
from cvp.imgui.button import button
from cvp.imgui.calc_button_size import calc_button_size
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.style_var import ITEM_SPACING
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS, TableFlags
from cvp.imgui.flags.table_column import WIDTH_FIXED, WIDTH_STRETCH
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.variables import NOT_FOUND_INDEX

_KT = TypeVar("_KT")


def default_table_item_input(
    index: int,
    item: Any,
    container: MutableSequence[_KT],
) -> None:
    imgui.set_next_item_width(FIT_WIDTH)

    if isinstance(item, str):
        if item_result := input_text(f"##Item.{index}", item):
            container[index] = item_result.value
    elif isinstance(item, int):
        if item_result := input_int(f"##Item.{index}", item):
            container[index] = item_result.value
    elif isinstance(item, float):
        if item_result := input_float(f"##Item.{index}", item):
            container[index] = item_result.value
    else:
        imgui.text(str(item))
        item_typename = type(item).__name__
        hovered_tooltip_text(f"The {item_typename} class does not support editing")


def table_mutable_sequence(
    label: str,
    container: MutableSequence[_KT],
    flags: Union[TableFlags, int] = DEFAULT_TABLE_FLAGS,
    outer_size: Optional[imgui.ImVec2Like] = None,
    inner_width: float = 0.0,
    swappable=False,
    removable=False,
    item_callback=default_table_item_input,
    insertable_callback: Optional[Callable[[int], Any]] = None,
    action_button_spacing=1.0,
):
    if isinstance(flags, TableFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if imgui.begin_table(label, 3, flags, outer_size, inner_width):
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

            imgui.table_setup_column("Index", WIDTH_FIXED)
            imgui.table_setup_column("Value", WIDTH_STRETCH)
            imgui.table_setup_column("Actions", WIDTH_FIXED, actions_width)
            imgui.table_headers_row()

            remove_index = NOT_FOUND_INDEX
            swap_tuple: Optional[Tuple[int, int]] = None
            insert_tuple: Optional[Tuple[int, Any]] = None
            last_index = len(container) - 1

            for i, item in enumerate(container):
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(str(i))

                imgui.table_set_column_index(1)
                item_callback(i, item, container)

                imgui.table_set_column_index(2)

                with begin_group_context():
                    no_up = not swappable or i == 0
                    no_down = not swappable or i == last_index
                    no_insert = insertable_callback is None
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
                            assert insertable_callback is not None
                            insert_tuple = i, insertable_callback(i)
                        hovered_tooltip_text(f"Insert a new item at position {i}")

                        imgui.same_line()
                        if button(f"{DELETE}###Del.{i}", disabled=no_remove):
                            remove_index = i
                        hovered_tooltip_text(f"Delete the item at position {i}")
                    finally:
                        imgui.pop_style_var()

            if insert_tuple is not None:
                i, new_item = insert_tuple
                container.insert(i, new_item)

            if swap_tuple is not None:
                left, right = swap_tuple
                temp = container[left]
                container[left] = container[right]
                container[right] = temp

            if remove_index != NOT_FOUND_INDEX:
                container.pop(remove_index)
        finally:
            imgui.end_table()

        if insertable_callback is not None:
            if imgui.button(f"{PLUS}##AppendNewItem"):
                container.append(insertable_callback(len(container)))

# -*- coding: utf-8 -*-

from typing import Any, Callable, MutableSequence, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS, TableFlags
from cvp.imgui.widgets.table_mutable_sequence import (
    _KT,
    default_table_item_input,
    table_mutable_sequence,
)


def begin_table_mutable_sequence(
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
    border=False,
    table_label="Table",
) -> None:
    with begin_child_context(
        label=label,
        size=(imgui.calc_item_width(), 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        table_mutable_sequence(
            label=table_label,
            container=container,
            flags=flags,
            outer_size=outer_size,
            inner_width=inner_width,
            swappable=swappable,
            removable=removable,
            item_callback=item_callback,
            insertable_callback=insertable_callback,
            action_button_spacing=action_button_spacing,
        )
    imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
    imgui.text(label)

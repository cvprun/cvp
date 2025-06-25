# -*- coding: utf-8 -*-

from typing import MutableMapping, Optional

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.widgets.table_mutable_mapping import (
    _KT,
    _VT,
    AddableFactoryCallable,
    FilterCallable,
    TableMutableMappingOptions,
    table_mutable_mapping,
)


def begin_table_mutable_mapping(
    label: str,
    container: MutableMapping[_KT, _VT],
    options: Optional[TableMutableMappingOptions] = None,
    *,
    addable_factory: Optional[AddableFactoryCallable] = None,
    filter_callback: Optional[FilterCallable] = None,
    removable: Optional[bool] = None,
    show_key: Optional[bool] = None,
    show_value: Optional[bool] = None,
    show_actions: Optional[bool] = None,
    disabled_value: Optional[bool] = None,
    border=False,
    table_label="Table",
):
    with begin_child_context(
        label=label,
        size=(imgui.calc_item_width(), 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        result = table_mutable_mapping(
            label=table_label,
            container=container,
            options=options,
            addable_factory=addable_factory,
            filter_callback=filter_callback,
            removable=removable,
            show_key=show_key,
            show_value=show_value,
            show_actions=show_actions,
            disabled_value=disabled_value,
        )
    imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
    imgui.text(label)
    return result

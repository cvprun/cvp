# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class DragDropFlags(IntFlag):
    # fmt:off
    none = imgui.DragDropFlags_.none.value
    source_no_preview_tooltip = imgui.DragDropFlags_.source_no_preview_tooltip.value
    source_no_disable_hover = imgui.DragDropFlags_.source_no_disable_hover.value
    source_no_hold_to_open_others = imgui.DragDropFlags_.source_no_hold_to_open_others.value  # noqa: E501
    source_allow_null_id = imgui.DragDropFlags_.source_allow_null_id.value
    source_extern = imgui.DragDropFlags_.source_extern.value
    payload_auto_expire = imgui.DragDropFlags_.payload_auto_expire.value
    payload_no_cross_context = imgui.DragDropFlags_.payload_no_cross_context.value
    payload_no_cross_process = imgui.DragDropFlags_.payload_no_cross_process.value
    accept_before_delivery = imgui.DragDropFlags_.accept_before_delivery.value
    accept_no_draw_default_rect = imgui.DragDropFlags_.accept_no_draw_default_rect.value
    accept_no_preview_tooltip = imgui.DragDropFlags_.accept_no_preview_tooltip.value
    accept_peek_only = imgui.DragDropFlags_.accept_peek_only.value
    # fmt:on


# fmt:off
NONE: Final[int] = int(DragDropFlags.none)
SOURCE_NO_PREVIEW_TOOLTIP: Final[int] = int(DragDropFlags.source_no_preview_tooltip)
SOURCE_NO_DISABLE_HOVER: Final[int] = int(DragDropFlags.source_no_disable_hover)
SOURCE_NO_HOLD_TO_OPEN_OTHERS: Final[int] = int(DragDropFlags.source_no_hold_to_open_others)  # noqa: E501
SOURCE_ALLOW_NULL_ID: Final[int] = int(DragDropFlags.source_allow_null_id)
SOURCE_EXTERN: Final[int] = int(DragDropFlags.source_extern)
PAYLOAD_AUTO_EXPIRE: Final[int] = int(DragDropFlags.payload_auto_expire)
PAYLOAD_NO_CROSS_CONTEXT: Final[int] = int(DragDropFlags.payload_no_cross_context)
PAYLOAD_NO_CROSS_PROCESS: Final[int] = int(DragDropFlags.payload_no_cross_process)
ACCEPT_BEFORE_DELIVERY: Final[int] = int(DragDropFlags.accept_before_delivery)
ACCEPT_NO_DRAW_DEFAULT_RECT: Final[int] = int(DragDropFlags.accept_no_draw_default_rect)
ACCEPT_NO_PREVIEW_TOOLTIP: Final[int] = int(DragDropFlags.accept_no_preview_tooltip)
ACCEPT_PEEK_ONLY: Final[int] = int(DragDropFlags.accept_peek_only)
# fmt:on


def merge_drag_drop_flags(*flags: Union[DragDropFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))

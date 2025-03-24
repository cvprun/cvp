# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class StyleVar(IntEnum):
    # fmt: off
    alpha = imgui.StyleVar_.alpha.value
    disabled_alpha = imgui.StyleVar_.disabled_alpha.value
    window_padding = imgui.StyleVar_.window_padding.value
    window_rounding = imgui.StyleVar_.window_rounding.value
    window_border_size = imgui.StyleVar_.window_border_size.value
    window_min_size = imgui.StyleVar_.window_min_size.value
    window_title_align = imgui.StyleVar_.window_title_align.value
    child_rounding = imgui.StyleVar_.child_rounding.value
    child_border_size = imgui.StyleVar_.child_border_size.value
    popup_rounding = imgui.StyleVar_.popup_rounding.value
    popup_border_size = imgui.StyleVar_.popup_border_size.value
    frame_padding = imgui.StyleVar_.frame_padding.value
    frame_rounding = imgui.StyleVar_.frame_rounding.value
    frame_border_size = imgui.StyleVar_.frame_border_size.value
    item_spacing = imgui.StyleVar_.item_spacing.value
    item_inner_spacing = imgui.StyleVar_.item_inner_spacing.value
    indent_spacing = imgui.StyleVar_.indent_spacing.value
    cell_padding = imgui.StyleVar_.cell_padding.value
    scrollbar_size = imgui.StyleVar_.scrollbar_size.value
    scrollbar_rounding = imgui.StyleVar_.scrollbar_rounding.value
    grab_min_size = imgui.StyleVar_.grab_min_size.value
    grab_rounding = imgui.StyleVar_.grab_rounding.value
    layout_align = imgui.StyleVar_.layout_align.value
    tab_rounding = imgui.StyleVar_.tab_rounding.value
    tab_border_size = imgui.StyleVar_.tab_border_size.value
    tab_bar_border_size = imgui.StyleVar_.tab_bar_border_size.value
    tab_bar_overline_size = imgui.StyleVar_.tab_bar_overline_size.value
    table_angled_headers_angle = imgui.StyleVar_.table_angled_headers_angle.value
    table_angled_headers_text_align = imgui.StyleVar_.table_angled_headers_text_align.value  # noqa: E501
    button_text_align = imgui.StyleVar_.button_text_align.value
    selectable_text_align = imgui.StyleVar_.selectable_text_align.value
    separator_text_border_size = imgui.StyleVar_.separator_text_border_size.value
    separator_text_align = imgui.StyleVar_.separator_text_align.value
    separator_text_padding = imgui.StyleVar_.separator_text_padding.value
    docking_separator_size = imgui.StyleVar_.docking_separator_size.value
    count = imgui.StyleVar_.count.value
    # fmt: on


# fmt: off
ALPHA: Final[int] = int(StyleVar.alpha)
DISABLED_ALPHA: Final[int] = int(StyleVar.disabled_alpha)
WINDOW_PADDING: Final[int] = int(StyleVar.window_padding)
WINDOW_ROUNDING: Final[int] = int(StyleVar.window_rounding)
WINDOW_BORDER_SIZE: Final[int] = int(StyleVar.window_border_size)
WINDOW_MIN_SIZE: Final[int] = int(StyleVar.window_min_size)
WINDOW_TITLE_ALIGN: Final[int] = int(StyleVar.window_title_align)
CHILD_ROUNDING: Final[int] = int(StyleVar.child_rounding)
CHILD_BORDER_SIZE: Final[int] = int(StyleVar.child_border_size)
POPUP_ROUNDING: Final[int] = int(StyleVar.popup_rounding)
POPUP_BORDER_SIZE: Final[int] = int(StyleVar.popup_border_size)
FRAME_PADDING: Final[int] = int(StyleVar.frame_padding)
FRAME_ROUNDING: Final[int] = int(StyleVar.frame_rounding)
FRAME_BORDER_SIZE: Final[int] = int(StyleVar.frame_border_size)
ITEM_SPACING: Final[int] = int(StyleVar.item_spacing)
ITEM_INNER_SPACING: Final[int] = int(StyleVar.item_inner_spacing)
INDENT_SPACING: Final[int] = int(StyleVar.indent_spacing)
CELL_PADDING: Final[int] = int(StyleVar.cell_padding)
SCROLLBAR_SIZE: Final[int] = int(StyleVar.scrollbar_size)
SCROLLBAR_ROUNDING: Final[int] = int(StyleVar.scrollbar_rounding)
GRAB_MIN_SIZE: Final[int] = int(StyleVar.grab_min_size)
GRAB_ROUNDING: Final[int] = int(StyleVar.grab_rounding)
LAYOUT_ALIGN: Final[int] = int(StyleVar.layout_align)
TAB_ROUNDING: Final[int] = int(StyleVar.tab_rounding)
TAB_BORDER_SIZE: Final[int] = int(StyleVar.tab_border_size)
TAB_BAR_BORDER_SIZE: Final[int] = int(StyleVar.tab_bar_border_size)
TAB_BAR_OVERLINE_SIZE: Final[int] = int(StyleVar.tab_bar_overline_size)
TABLE_ANGLED_HEADERS_ANGLE: Final[int] = int(StyleVar.table_angled_headers_angle)
TABLE_ANGLED_HEADERS_TEXT_ALIGN: Final[int] = int(StyleVar.table_angled_headers_text_align)  # noqa: E501
BUTTON_TEXT_ALIGN: Final[int] = int(StyleVar.button_text_align)
SELECTABLE_TEXT_ALIGN: Final[int] = int(StyleVar.selectable_text_align)
SEPARATOR_TEXT_BORDER_SIZE: Final[int] = int(StyleVar.separator_text_border_size)
SEPARATOR_TEXT_ALIGN: Final[int] = int(StyleVar.separator_text_align)
SEPARATOR_TEXT_PADDING: Final[int] = int(StyleVar.separator_text_padding)
DOCKING_SEPARATOR_SIZE: Final[int] = int(StyleVar.docking_separator_size)
COUNT: Final[int] = int(StyleVar.count)
# fmt: on

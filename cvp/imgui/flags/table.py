# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class TableFlags(IntFlag):
    # fmt: off
    none = imgui.TableFlags_.none.value
    resizable = imgui.TableFlags_.resizable.value
    reorderable = imgui.TableFlags_.reorderable.value
    hideable = imgui.TableFlags_.hideable.value
    sortable = imgui.TableFlags_.sortable.value
    no_saved_settings = imgui.TableFlags_.no_saved_settings.value
    context_menu_in_body = imgui.TableFlags_.context_menu_in_body.value
    row_bg = imgui.TableFlags_.row_bg.value
    borders_inner_h = imgui.TableFlags_.borders_inner_h.value
    borders_outer_h = imgui.TableFlags_.borders_outer_h.value
    borders_inner_v = imgui.TableFlags_.borders_inner_v.value
    borders_outer_v = imgui.TableFlags_.borders_outer_v.value
    borders_h = imgui.TableFlags_.borders_h.value
    borders_v = imgui.TableFlags_.borders_v.value
    borders_inner = imgui.TableFlags_.borders_inner.value
    borders_outer = imgui.TableFlags_.borders_outer.value
    borders = imgui.TableFlags_.borders.value
    no_borders_in_body = imgui.TableFlags_.no_borders_in_body.value
    no_borders_in_body_until_resize = imgui.TableFlags_.no_borders_in_body_until_resize.value  # noqa: E501
    sizing_fixed_fit = imgui.TableFlags_.sizing_fixed_fit.value
    sizing_fixed_same = imgui.TableFlags_.sizing_fixed_same.value
    sizing_stretch_prop = imgui.TableFlags_.sizing_stretch_prop.value
    sizing_stretch_same = imgui.TableFlags_.sizing_stretch_same.value
    no_host_extend_x = imgui.TableFlags_.no_host_extend_x.value
    no_host_extend_y = imgui.TableFlags_.no_host_extend_y.value
    no_keep_columns_visible = imgui.TableFlags_.no_keep_columns_visible.value
    precise_widths = imgui.TableFlags_.precise_widths.value
    no_clip = imgui.TableFlags_.no_clip.value
    pad_outer_x = imgui.TableFlags_.pad_outer_x.value
    no_pad_outer_x = imgui.TableFlags_.no_pad_outer_x.value
    no_pad_inner_x = imgui.TableFlags_.no_pad_inner_x.value
    scroll_x = imgui.TableFlags_.scroll_x.value
    scroll_y = imgui.TableFlags_.scroll_y.value
    sort_multi = imgui.TableFlags_.sort_multi.value
    sort_tristate = imgui.TableFlags_.sort_tristate.value
    highlight_hovered_column = imgui.TableFlags_.highlight_hovered_column.value
    # fmt: on

    # [Internal]
    sizing_mask_ = imgui.TableFlags_.sizing_mask_.value


# fmt: off
NONE: Final[int] = int(TableFlags.none)
RESIZABLE: Final[int] = int(TableFlags.resizable)
REORDERABLE: Final[int] = int(TableFlags.reorderable)
HIDEABLE: Final[int] = int(TableFlags.hideable)
SORTABLE: Final[int] = int(TableFlags.sortable)
NO_SAVED_SETTINGS: Final[int] = int(TableFlags.no_saved_settings)
CONTEXT_MENU_IN_BODY: Final[int] = int(TableFlags.context_menu_in_body)
ROW_BG: Final[int] = int(TableFlags.row_bg)
BORDERS_INNER_H: Final[int] = int(TableFlags.borders_inner_h)
BORDERS_OUTER_H: Final[int] = int(TableFlags.borders_outer_h)
BORDERS_INNER_V: Final[int] = int(TableFlags.borders_inner_v)
BORDERS_OUTER_V: Final[int] = int(TableFlags.borders_outer_v)
BORDERS_H: Final[int] = int(TableFlags.borders_h)
BORDERS_V: Final[int] = int(TableFlags.borders_v)
BORDERS_INNER: Final[int] = int(TableFlags.borders_inner)
BORDERS_OUTER: Final[int] = int(TableFlags.borders_outer)
BORDERS: Final[int] = int(TableFlags.borders)
NO_BORDERS_IN_BODY: Final[int] = int(TableFlags.no_borders_in_body)
NO_BORDERS_IN_BODY_UNTIL_RESIZE: Final[int] = int(TableFlags.no_borders_in_body_until_resize)  # noqa: E501
SIZING_FIXED_FIT: Final[int] = int(TableFlags.sizing_fixed_fit)
SIZING_FIXED_SAME: Final[int] = int(TableFlags.sizing_fixed_same)
SIZING_STRETCH_PROP: Final[int] = int(TableFlags.sizing_stretch_prop)
SIZING_STRETCH_SAME: Final[int] = int(TableFlags.sizing_stretch_same)
NO_HOST_EXTEND_X: Final[int] = int(TableFlags.no_host_extend_x)
NO_HOST_EXTEND_Y: Final[int] = int(TableFlags.no_host_extend_y)
NO_KEEP_COLUMNS_VISIBLE: Final[int] = int(TableFlags.no_keep_columns_visible)
PRECISE_WIDTHS: Final[int] = int(TableFlags.precise_widths)
NO_CLIP: Final[int] = int(TableFlags.no_clip)
PAD_OUTER_X: Final[int] = int(TableFlags.pad_outer_x)
NO_PAD_OUTER_X: Final[int] = int(TableFlags.no_pad_outer_x)
NO_PAD_INNER_X: Final[int] = int(TableFlags.no_pad_inner_x)
SCROLL_X: Final[int] = int(TableFlags.scroll_x)
SCROLL_Y: Final[int] = int(TableFlags.scroll_y)
SORT_MULTI: Final[int] = int(TableFlags.sort_multi)
SORT_TRISTATE: Final[int] = int(TableFlags.sort_tristate)
HIGHLIGHT_HOVERED_COLUMN: Final[int] = int(TableFlags.highlight_hovered_column)
# fmt: on


def merge_table_flags(*flags: Union[TableFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))


ONVIF_TABLE_FLAGS: Final[int] = merge_table_flags(
    TableFlags.sizing_fixed_fit,
    TableFlags.row_bg,
    TableFlags.borders,
    TableFlags.resizable,
    TableFlags.reorderable,
    TableFlags.hideable,
)

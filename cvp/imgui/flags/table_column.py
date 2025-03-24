# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class TableColumnFlags(IntFlag):
    # Input configuration flags
    none = imgui.TableColumnFlags_.none.value
    disabled = imgui.TableColumnFlags_.disabled.value
    default_hide = imgui.TableColumnFlags_.default_hide.value
    default_sort = imgui.TableColumnFlags_.default_sort.value
    width_stretch = imgui.TableColumnFlags_.width_stretch.value
    width_fixed = imgui.TableColumnFlags_.width_fixed.value
    no_resize = imgui.TableColumnFlags_.no_resize.value
    no_reorder = imgui.TableColumnFlags_.no_reorder.value
    no_hide = imgui.TableColumnFlags_.no_hide.value
    no_clip = imgui.TableColumnFlags_.no_clip.value
    no_sort = imgui.TableColumnFlags_.no_sort.value
    no_sort_ascending = imgui.TableColumnFlags_.no_sort_ascending.value
    no_sort_descending = imgui.TableColumnFlags_.no_sort_descending.value
    no_header_label = imgui.TableColumnFlags_.no_header_label.value
    no_header_width = imgui.TableColumnFlags_.no_header_width.value
    prefer_sort_ascending = imgui.TableColumnFlags_.prefer_sort_ascending.value
    prefer_sort_descending = imgui.TableColumnFlags_.prefer_sort_descending.value
    indent_enable = imgui.TableColumnFlags_.indent_enable.value
    indent_disable = imgui.TableColumnFlags_.indent_disable.value
    angled_header = imgui.TableColumnFlags_.angled_header.value

    # Output status flags, read-only via TableGetColumnFlags()
    is_enabled = imgui.TableColumnFlags_.is_enabled.value
    is_visible = imgui.TableColumnFlags_.is_visible.value
    is_sorted = imgui.TableColumnFlags_.is_sorted.value
    is_hovered = imgui.TableColumnFlags_.is_hovered.value

    # [Internal] Combinations and masks
    width_mask_ = imgui.TableColumnFlags_.width_mask_.value
    indent_mask_ = imgui.TableColumnFlags_.indent_mask_.value
    status_mask_ = imgui.TableColumnFlags_.status_mask_.value
    no_direct_resize_ = imgui.TableColumnFlags_.no_direct_resize_.value


NONE: Final[int] = int(TableColumnFlags.none)
DISABLED: Final[int] = int(TableColumnFlags.disabled)
DEFAULT_HIDE: Final[int] = int(TableColumnFlags.default_hide)
DEFAULT_SORT: Final[int] = int(TableColumnFlags.default_sort)
WIDTH_STRETCH: Final[int] = int(TableColumnFlags.width_stretch)
WIDTH_FIXED: Final[int] = int(TableColumnFlags.width_fixed)
NO_RESIZE: Final[int] = int(TableColumnFlags.no_resize)
NO_REORDER: Final[int] = int(TableColumnFlags.no_reorder)
NO_HIDE: Final[int] = int(TableColumnFlags.no_hide)
NO_CLIP: Final[int] = int(TableColumnFlags.no_clip)
NO_SORT: Final[int] = int(TableColumnFlags.no_sort)
NO_SORT_ASCENDING: Final[int] = int(TableColumnFlags.no_sort_ascending)
NO_SORT_DESCENDING: Final[int] = int(TableColumnFlags.no_sort_descending)
NO_HEADER_LABEL: Final[int] = int(TableColumnFlags.no_header_label)
NO_HEADER_WIDTH: Final[int] = int(TableColumnFlags.no_header_width)
PREFER_SORT_ASCENDING: Final[int] = int(TableColumnFlags.prefer_sort_ascending)
PREFER_SORT_DESCENDING: Final[int] = int(TableColumnFlags.prefer_sort_descending)
INDENT_ENABLE: Final[int] = int(TableColumnFlags.indent_enable)
INDENT_DISABLE: Final[int] = int(TableColumnFlags.indent_disable)
ANGLED_HEADER: Final[int] = int(TableColumnFlags.angled_header)
IS_ENABLED: Final[int] = int(TableColumnFlags.is_enabled)
IS_VISIBLE: Final[int] = int(TableColumnFlags.is_visible)
IS_SORTED: Final[int] = int(TableColumnFlags.is_sorted)
IS_HOVERED: Final[int] = int(TableColumnFlags.is_hovered)


def merge_table_column_flags(*flags: Union[TableColumnFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))

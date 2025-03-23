# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Sequence, Union

from imgui_bundle import imgui


@unique
class TreeNodeFlags(IntFlag):
    none = imgui.TreeNodeFlags_.none.value
    selected = imgui.TreeNodeFlags_.selected.value
    framed = imgui.TreeNodeFlags_.framed.value
    allow_overlap = imgui.TreeNodeFlags_.allow_overlap.value
    no_tree_push_on_open = imgui.TreeNodeFlags_.no_tree_push_on_open.value
    no_auto_open_on_log = imgui.TreeNodeFlags_.no_auto_open_on_log.value
    default_open = imgui.TreeNodeFlags_.default_open.value
    open_on_double_click = imgui.TreeNodeFlags_.open_on_double_click.value
    open_on_arrow = imgui.TreeNodeFlags_.open_on_arrow.value
    leaf = imgui.TreeNodeFlags_.leaf.value
    bullet = imgui.TreeNodeFlags_.bullet.value
    frame_padding = imgui.TreeNodeFlags_.frame_padding.value
    span_avail_width = imgui.TreeNodeFlags_.span_avail_width.value
    span_full_width = imgui.TreeNodeFlags_.span_full_width.value
    span_text_width = imgui.TreeNodeFlags_.span_text_width.value
    span_all_columns = imgui.TreeNodeFlags_.span_all_columns.value
    nav_left_jumps_back_here = imgui.TreeNodeFlags_.nav_left_jumps_back_here.value
    collapsing_header = imgui.TreeNodeFlags_.collapsing_header.value


NONE: Final[int] = int(TreeNodeFlags.none)
SELECTED: Final[int] = int(TreeNodeFlags.selected)
FRAMED: Final[int] = int(TreeNodeFlags.framed)
ALLOW_OVERLAP: Final[int] = int(TreeNodeFlags.allow_overlap)
NO_TREE_PUSH_ON_OPEN: Final[int] = int(TreeNodeFlags.no_tree_push_on_open)
NO_AUTO_OPEN_ON_LOG: Final[int] = int(TreeNodeFlags.no_auto_open_on_log)
DEFAULT_OPEN: Final[int] = int(TreeNodeFlags.default_open)
OPEN_ON_DOUBLE_CLICK: Final[int] = int(TreeNodeFlags.open_on_double_click)
OPEN_ON_ARROW: Final[int] = int(TreeNodeFlags.open_on_arrow)
LEAF: Final[int] = int(TreeNodeFlags.leaf)
BULLET: Final[int] = int(TreeNodeFlags.bullet)
FRAME_PADDING: Final[int] = int(TreeNodeFlags.frame_padding)
SPAN_AVAIL_WIDTH: Final[int] = int(TreeNodeFlags.span_avail_width)
SPAN_FULL_WIDTH: Final[int] = int(TreeNodeFlags.span_full_width)
SPAN_TEXT_WIDTH: Final[int] = int(TreeNodeFlags.span_text_width)
SPAN_ALL_COLUMNS: Final[int] = int(TreeNodeFlags.span_all_columns)
NAV_LEFT_JUMPS_BACK_HERE: Final[int] = int(TreeNodeFlags.nav_left_jumps_back_here)
COLLAPSING_HEADER: Final[int] = int(TreeNodeFlags.collapsing_header)


def merge_tree_node_flags(*flags: Union[TreeNodeFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))


_COMMON_FLAGS: Final[Sequence[TreeNodeFlags]] = (
    TreeNodeFlags.open_on_arrow,
    TreeNodeFlags.open_on_double_click,
    TreeNodeFlags.span_avail_width,
)
_LEAF_FLAGS: Final[Sequence[TreeNodeFlags]] = (
    TreeNodeFlags.open_on_arrow,
    TreeNodeFlags.open_on_double_click,
    TreeNodeFlags.span_avail_width,
    TreeNodeFlags.leaf,
    TreeNodeFlags.no_tree_push_on_open,
)

CATEGORY_FLAGS: Final[int] = merge_tree_node_flags(*_COMMON_FLAGS, DEFAULT_OPEN)
NODE_FLAGS: Final[int] = merge_tree_node_flags(*_COMMON_FLAGS)
PIN_FLAGS: Final[int] = merge_tree_node_flags(*_LEAF_FLAGS)
ARC_FLAGS: Final[int] = merge_tree_node_flags(*_LEAF_FLAGS)
VARIABLE_FLAGS: Final[int] = merge_tree_node_flags(*_LEAF_FLAGS)

# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class DockNodeFlags(IntFlag):
    # fmt: off
    none = imgui.DockNodeFlags_.none.value
    keep_alive_only = imgui.DockNodeFlags_.keep_alive_only.value
    no_docking_over_central_node = imgui.DockNodeFlags_.no_docking_over_central_node.value  # noqa: E501
    passthru_central_node = imgui.DockNodeFlags_.passthru_central_node.value
    no_docking_split = imgui.DockNodeFlags_.no_docking_split.value
    no_resize = imgui.DockNodeFlags_.no_resize.value
    auto_hide_tab_bar = imgui.DockNodeFlags_.auto_hide_tab_bar.value
    no_undocking = imgui.DockNodeFlags_.no_undocking.value
    # fmt: on


# fmt: off
NONE: Final[int] = int(DockNodeFlags.none)
KEEP_ALIVE_ONLY: Final[int] = int(DockNodeFlags.keep_alive_only)
NO_DOCKING_OVER_CENTRAL_NODE: Final[int] = int(DockNodeFlags.no_docking_over_central_node)  # noqa: E501
PASSTHRU_CENTRAL_NODE: Final[int] = int(DockNodeFlags.passthru_central_node)
NO_DOCKING_SPLIT: Final[int] = int(DockNodeFlags.no_docking_split)
NO_RESIZE: Final[int] = int(DockNodeFlags.no_resize)
AUTO_HIDE_TAB_BAR: Final[int] = int(DockNodeFlags.auto_hide_tab_bar)
NO_UNDOCKING: Final[int] = int(DockNodeFlags.no_undocking)
# fmt: on


def merge_dock_node_flags(*flags: Union[DockNodeFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))


DOCKSPACE_FLAGS: Final[int] = merge_dock_node_flags(
    PASSTHRU_CENTRAL_NODE,
    NO_DOCKING_OVER_CENTRAL_NODE,
)

# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

DOCK_SPACE_FLAG: Final[int] = int(imgui.internal.DockNodeFlagsPrivate_.dock_space.value)
DOCKING_ENABLE_FLAG: Final[int] = int(imgui.ConfigFlags_.docking_enable.value)


def enabled_docking_flag() -> bool:
    return bool(imgui.get_io().config_flags & DOCKING_ENABLE_FLAG)


def remove_node(node_id: int) -> None:
    imgui.internal.dock_builder_remove_node(node_id)


def add_node(node_id: int, flags=0) -> int:
    return imgui.internal.dock_builder_add_node(node_id, flags)


def add_dock_space_node(node_id: int, flags=0) -> int:
    return add_node(node_id, DOCK_SPACE_FLAG | flags)


def set_node_size(node_id: int, size: imgui.ImVec2Like) -> None:
    imgui.internal.dock_builder_set_node_size(node_id, size)


def get_node(node_id: int):
    return imgui.internal.dock_builder_get_node(node_id)


def split_node(node_id: int, split_dir: imgui.Dir, ratio: float):
    return imgui.internal.dock_builder_split_node(node_id, split_dir, ratio)


def dock_window(window_name: str, node_id: int) -> None:
    imgui.internal.dock_builder_dock_window(window_name, node_id)


def finish(node_id: int) -> None:
    imgui.internal.dock_builder_finish(node_id)

# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def split_node(node_id: int, split_dir: imgui.Dir, ratio: float):
    return imgui.internal.dock_builder_split_node(node_id, split_dir, ratio)


def dock_window(window_name: str, node_id: int) -> None:
    imgui.internal.dock_builder_dock_window(window_name, node_id)

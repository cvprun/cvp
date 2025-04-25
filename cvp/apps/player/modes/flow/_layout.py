# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Final, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow, FlowWindowInterface
from cvp.context.context import Context

DOCK_SPACE_FLAG: Final[int] = int(imgui.internal.DockNodeFlagsPrivate_.dock_space.value)
DOCKING_ENABLE_FLAG: Final[int] = int(imgui.ConfigFlags_.docking_enable.value)


def split_node(node_id: int, split_dir: imgui.Dir, ratio: float):
    return imgui.internal.dock_builder_split_node(node_id, split_dir, ratio)


def dock_window(window_name: str, node_id: int) -> None:
    imgui.internal.dock_builder_dock_window(window_name, node_id)


class _FlowLayout:
    types: Sequence[Type[BaseFlowWindow]]

    def __init__(self):
        from cvp.apps.player.modes.flow.catalog import CatalogFlowWindow
        from cvp.apps.player.modes.flow.debug import DebugFlowWindow
        from cvp.apps.player.modes.flow.history import HistoryFlowWindow
        from cvp.apps.player.modes.flow.intro import IntroFlowWindow
        from cvp.apps.player.modes.flow.logging import LoggingFlowWindow
        from cvp.apps.player.modes.flow.props import PropsFlowWindow
        from cvp.apps.player.modes.flow.tree import TreeFlowWindow

        self._initialized_dock_layout = False

        self.catalog = CatalogFlowWindow.get_window_name()
        self.debug = DebugFlowWindow.get_window_name()
        self.history = HistoryFlowWindow.get_window_name()
        self.intro = IntroFlowWindow.get_window_name()
        self.logging = LoggingFlowWindow.get_window_name()
        self.props = PropsFlowWindow.get_window_name()
        self.tree = TreeFlowWindow.get_window_name()

        self.types = (
            CatalogFlowWindow,
            DebugFlowWindow,
            HistoryFlowWindow,
            IntroFlowWindow,
            LoggingFlowWindow,
            PropsFlowWindow,
            TreeFlowWindow,
        )

    @property
    def initialized(self) -> bool:
        return self._initialized_dock_layout

    def create_windows(self, context: Context) -> OrderedDict[str, FlowWindowInterface]:
        return OrderedDict({wt.get_window_name(): wt(context) for wt in self.types})

    def _initialize_dock_layout(
        self,
        dockspace_id: int,
        viewport: imgui.Viewport,
        left_ratio=0.15,
        right_ratio=0.15,
        left_up_ratio=0.60,
        right_up_ratio=0.60,
        bottom_ratio=0.25,
    ) -> None:
        imgui.internal.dock_builder_add_node(dockspace_id, DOCK_SPACE_FLAG)
        imgui.internal.dock_builder_set_node_size(dockspace_id, viewport.work_size)

        split_result = split_node(dockspace_id, imgui.Dir.left, left_ratio)
        dock_left = split_result.id_at_dir
        dock_main_right = split_result.id_at_opposite_dir

        split_result = split_node(dock_main_right, imgui.Dir.right, right_ratio)
        dock_right = split_result.id_at_dir
        dock_center = split_result.id_at_opposite_dir

        split_result = split_node(dock_left, imgui.Dir.up, left_up_ratio)
        dock_left_top = split_result.id_at_dir
        dock_left_bottom = split_result.id_at_opposite_dir

        split_result = split_node(dock_right, imgui.Dir.up, right_up_ratio)
        dock_right_top = split_result.id_at_dir
        dock_right_bottom = split_result.id_at_opposite_dir

        split_result = split_node(dock_center, imgui.Dir.down, bottom_ratio)
        dock_center_bottom = split_result.id_at_dir
        dock_center_top = split_result.id_at_opposite_dir

        dock_window(self.tree, dock_left_top)
        dock_window(self.catalog, dock_left_bottom)

        dock_window(self.props, dock_right_top)
        dock_window(self.history, dock_right_bottom)

        dock_window(self.logging, dock_center_bottom)
        dock_window(self.debug, dock_center_bottom)

        dock_window(self.intro, dock_center_top)

        # dock_left_top_node = imgui.internal.dock_builder_get_node(dock_left_top)
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_docking_split
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_resize
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_undocking

    @staticmethod
    def enabled_docking() -> bool:
        return bool(imgui.get_io().config_flags & DOCKING_ENABLE_FLAG)

    def initialize_dock_layout(
        self,
        dockspace_id: int,
        viewport: imgui.Viewport,
    ) -> None:
        if not self.enabled_docking():
            return

        if self._initialized_dock_layout:
            return

        imgui.internal.dock_builder_remove_node(dockspace_id)
        try:
            self._initialize_dock_layout(dockspace_id, viewport)
        finally:
            imgui.internal.dock_builder_finish(dockspace_id)
            self._initialized_dock_layout = True

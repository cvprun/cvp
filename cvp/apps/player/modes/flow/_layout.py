# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import FlowWindowInterface
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context

DOCK_SPACE_FLAG: Final[int] = int(imgui.internal.DockNodeFlagsPrivate_.dock_space.value)
DOCKING_ENABLE_FLAG: Final[int] = int(imgui.ConfigFlags_.docking_enable.value)


def split_node(node_id: int, split_dir: imgui.Dir, ratio: float):
    return imgui.internal.dock_builder_split_node(node_id, split_dir, ratio)


def dock_window(window_name: str, node_id: int) -> None:
    imgui.internal.dock_builder_dock_window(window_name, node_id)


class FlowLayout:
    _windows: Sequence[FlowWindowInterface]
    _main_dock_id: Optional[int]

    def __init__(self, context: Context):
        from cvp.apps.player.modes.flow.debug import DebugFlowWindow
        from cvp.apps.player.modes.flow.dtypes import DtypesFlowWindow
        from cvp.apps.player.modes.flow.graphs import GraphsFlowWindow
        from cvp.apps.player.modes.flow.history import HistoryFlowWindow
        from cvp.apps.player.modes.flow.intro import IntroFlowWindow
        from cvp.apps.player.modes.flow.logging import LoggingFlowWindow
        from cvp.apps.player.modes.flow.nodes import NodesFlowWindow
        from cvp.apps.player.modes.flow.props import PropsFlowWindow
        from cvp.apps.player.modes.flow.tree import TreeFlowWindow

        self._context = context
        self._initialized_dock_layout = False
        self._main_dock_id = None

        self.dtypes = DtypesFlowWindow(context)
        self.debug = DebugFlowWindow(context)
        self.graphs = GraphsFlowWindow(context)
        self.history = HistoryFlowWindow(context)
        self.intro = IntroFlowWindow(context)
        self.logging = LoggingFlowWindow(context)
        self.nodes = NodesFlowWindow(context)
        self.props = PropsFlowWindow(context)
        self.tree = TreeFlowWindow(context)

        self._windows = (
            # Left Dock
            self.tree,
            self.graphs,
            self.nodes,
            self.dtypes,
            # Right Dock
            self.props,
            self.history,
            # Bottom Dock
            self.logging,
            self.debug,
            # Main Dock
            self.intro,
        )

        self._graph_windows = FlowGraphWindow.create_opened_windows(context)

    @property
    def initialized(self) -> bool:
        return self._initialized_dock_layout

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

        dock_window(self.tree.get_window_name(), dock_left_top)
        dock_window(self.graphs.get_window_name(), dock_left_bottom)
        dock_window(self.dtypes.get_window_name(), dock_left_bottom)
        dock_window(self.nodes.get_window_name(), dock_left_bottom)

        dock_window(self.props.get_window_name(), dock_right_top)
        dock_window(self.history.get_window_name(), dock_right_bottom)

        dock_window(self.debug.get_window_name(), dock_center_bottom)
        dock_window(self.logging.get_window_name(), dock_center_bottom)

        dock_window(self.intro.get_window_name(), dock_center_top)
        for gw in self._graph_windows.values():
            dock_window(gw.get_window_name(), dock_center_top)
        self._main_dock_id = dock_center_top

        # dock_left_top_node = imgui.internal.dock_builder_get_node(dock_left_top)
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_docking_split
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_resize
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_undocking

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

    @staticmethod
    def enabled_docking() -> bool:
        return bool(imgui.get_io().config_flags & DOCKING_ENABLE_FLAG)

    @property
    def focused_graph_window(self):
        if focused_graph_key := self._context.flows.focused_graph_key:
            return self._graph_windows.get(focused_graph_key)
        else:
            return None

    def refresh_graphs(self) -> None:
        prev_keys = set(self._graph_windows.keys())
        self._graph_windows.clear()

        # -----------------------------------------
        self._context.flows.graphs.clear()
        self._context.flows.read_all_graph_files()
        # -----------------------------------------

        self._graph_windows = FlowGraphWindow.create_opened_windows(self._context)
        for gw_key, gw in self._graph_windows.items():
            if self._main_dock_id is not None and gw_key not in prev_keys:
                dock_window(gw.get_window_name(), self._main_dock_id)

    def do_process(self) -> None:
        fgw = self.focused_graph_window
        for window in self._windows:
            window.do_process(fgw)
        for gw in self._graph_windows.values():
            gw.do_process()

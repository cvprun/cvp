# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.apps.player.modes.flows.flow._base import FlowWindowInterface
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.flow.graph import GraphKey
from cvp.imgui.dock_builder import (
    add_dock_space_node,
    dock_window,
    enabled_docking_flag,
    finish,
    remove_node,
    set_node_size,
    split_node,
)
from cvp.imgui.dockspace import dockspace_over_viewport_context
from cvp.imgui.flags.dock_node import PASSTHRU_CENTRAL_NODE, DockNodeFlags


class FlowLayout:
    _LEFT_RATIO: Final[float] = 0.15
    _RIGHT_RATIO: Final[float] = 0.15
    _LEFT_UP_RATIO: Final[float] = 0.60
    _RIGHT_UP_RATIO: Final[float] = 0.60
    _BOTTOM_RATIO: Final[float] = 0.25

    _windows: Sequence[FlowWindowInterface]
    _main_dock_id: Optional[int]

    def __init__(self, context: Context):
        from cvp.apps.player.modes.flows.flow.debug import DebugFlowWindow
        from cvp.apps.player.modes.flows.flow.dtypes import DtypesFlowWindow
        from cvp.apps.player.modes.flows.flow.graphs import GraphsFlowWindow
        from cvp.apps.player.modes.flows.flow.history import HistoryFlowWindow
        from cvp.apps.player.modes.flows.flow.intro import IntroFlowWindow
        from cvp.apps.player.modes.flows.flow.logging import LoggingFlowWindow
        from cvp.apps.player.modes.flows.flow.nodes import NodesFlowWindow
        from cvp.apps.player.modes.flows.flow.props import PropsFlowWindow
        from cvp.apps.player.modes.flows.flow.tree import TreeFlowWindow

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
    ) -> None:
        add_dock_space_node(dockspace_id)
        set_node_size(dockspace_id, viewport.work_size)

        split_result = split_node(dockspace_id, imgui.Dir.left, self._LEFT_RATIO)
        dock_left = split_result.id_at_dir
        dock_main_right = split_result.id_at_opposite_dir

        split_result = split_node(dock_main_right, imgui.Dir.right, self._RIGHT_RATIO)
        dock_right = split_result.id_at_dir
        dock_center = split_result.id_at_opposite_dir

        split_result = split_node(dock_left, imgui.Dir.up, self._LEFT_UP_RATIO)
        dock_left_top = split_result.id_at_dir
        dock_left_bottom = split_result.id_at_opposite_dir

        split_result = split_node(dock_right, imgui.Dir.up, self._RIGHT_UP_RATIO)
        dock_right_top = split_result.id_at_dir
        dock_right_bottom = split_result.id_at_opposite_dir

        split_result = split_node(dock_center, imgui.Dir.down, self._BOTTOM_RATIO)
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
        if not enabled_docking_flag():
            return

        if self._initialized_dock_layout:
            return

        remove_node(dockspace_id)
        try:
            self._initialize_dock_layout(dockspace_id, viewport)
        finally:
            finish(dockspace_id)
            self._initialized_dock_layout = True

    @property
    def focused_window(self):
        if focused_key := self._context.flows.focused_key:
            return self._graph_windows.get(focused_key)
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

    def create_graph_window(self, key: GraphKey):
        graph_windows = FlowGraphWindow(self._context, key)
        self._graph_windows[key] = graph_windows
        if self._main_dock_id is not None:
            dock_window(graph_windows.get_window_name(), self._main_dock_id)
        return graph_windows

    def remove_graph_window(self, key: GraphKey):
        return self._graph_windows.pop(key)

    def sync_graph_windows(self) -> None:
        graph_keys = set(self._context.flows.graphs.keys())
        window_keys = set(self._graph_windows.keys())
        if graph_keys == window_keys:
            return

        for remove_key in window_keys - graph_keys:
            self.remove_graph_window(remove_key)

        for create_key in graph_keys - window_keys:
            self.create_graph_window(create_key)

        graph_keys = set(self._context.flows.graphs.keys())
        window_keys = set(self._graph_windows.keys())
        assert graph_keys == window_keys

    def do_process(
        self,
        dock_space_id: Optional[Union[str, int]] = None,
        viewport: Optional[imgui.Viewport] = None,
        flags: Union[DockNodeFlags, int] = PASSTHRU_CENTRAL_NODE,
        window_class: Optional[imgui.WindowClass] = None,
    ) -> None:
        if viewport is None:
            viewport = imgui.get_main_viewport()
        assert isinstance(viewport, imgui.Viewport)

        with dockspace_over_viewport_context(
            dock_space_id=dock_space_id,
            viewport=viewport,
            flags=flags,
            window_class=window_class,
        ) as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id
            if not self._initialized_dock_layout:
                self.initialize_dock_layout(dockspace_id, viewport)

        self.sync_graph_windows()

        focused_window = self.focused_window
        for window in self._windows:
            window.do_process(focused_window)

        for gw in self._graph_windows.values():
            gw.do_process()

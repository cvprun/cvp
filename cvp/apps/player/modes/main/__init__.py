# -*- coding: utf-8 -*-

from types import ModuleType
from typing import Callable, Dict, Final, Optional, Sequence, Tuple, Type

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.main import canvas, flow
from cvp.apps.player.modes.main.dashboard import DashboardWindow
from cvp.apps.player.modes.main.interface import (
    WindowInterface,
    retrieve_window_instances,
)
from cvp.canvas.canvas import CanvasKey
from cvp.context.context import Context
from cvp.flow.graph import GraphKey
from cvp.imgui.dock_builder import (
    add_dock_space_node,
    dock_window,
    enabled_docking_flag,
    finish,
    get_node,
    remove_node,
    set_node_size,
    split_node,
)
from cvp.imgui.dockspace import dockspace_over_viewport_context
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.msgs.msg import Msg
from cvp.types.override import override


class MainMode(BaseMode):
    __cvp_mode_name__ = "Main"

    _LEFT_RATIO: Final[float] = 0.15
    _RIGHT_RATIO: Final[float] = 0.15
    _LEFT_UP_RATIO: Final[float] = 0.60
    _RIGHT_UP_RATIO: Final[float] = 0.60
    _BOTTOM_RATIO: Final[float] = 0.25

    _central_dock_id: Optional[int]
    _prefix_menus: Sequence[Tuple[str, Callable[[], None]]]
    _suffix_menus: Sequence[Tuple[str, Callable[[], None]]]

    _tools: Dict[str, WindowInterface]
    _mains: Dict[str, WindowInterface]

    def __init__(self, context: Context):
        super().__init__(context)

        self._context = context
        self._initialized_dock_layout = False
        self._central_dock_id = None

        self._prefix_menus = (("File", self.on_file_menu),)
        self._suffix_menus = (("Window", self.on_window_menu),)

        # ==============================================================================
        # region: Initialize Window Instances
        # [IMPORTANT] Do not change the initialize order!

        self.dashboard = DashboardWindow(context)
        self.flow_dtype = flow.DtypeFlowWindow(context)
        self.flow_dtypes = flow.DtypesFlowWindow(context)
        self.flow_debug = flow.DebugFlowWindow(context)
        self.flow_graphs = flow.GraphsFlowWindow(context)
        self.flow_history = flow.HistoryFlowWindow(context)
        self.flow_logging = flow.LoggingFlowWindow(context)
        self.flow_node = flow.NodeFlowWindow(context)
        self.flow_nodes = flow.NodesFlowWindow(context)
        self.flow_props = flow.PropsFlowWindow(context)
        self.flow_tree = flow.TreeFlowWindow(context)

        # ------------------------------------------------------------------------------
        # Retrieves and stores all ModeInterface instances assigned to `self`
        self._tools = {w.get_window_name(): w for w in retrieve_window_instances(self)}
        # endregion: Initialize Window Instances
        # ==============================================================================

        self._mains = dict()
        self._mains.update(flow.GraphFlowWindow.create_opened_windows(context))
        self._mains.update(canvas.CanvasWindow.create_opened_windows(context))

        self._new_graph_popup = InputTextPopup(
            title="New graph",
            label="Please enter a graph name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_graph,
        )
        self._import_graph_popup = OpenFilePopup(
            title="Import graph",
            target=self.on_import_graph,
        )
        self._export_graph_popup = OpenFilePopup(
            title="Export graph",
            target=self.on_export_graph,
            open_mode=OpenFilePopup.OpenMode.input_filename,
        )
        self._confirm_remove_graph_popup = ConfirmPopup(
            title="Remove graph",
            label="Are you sure you want to remove graph?",
            ok="Remove",
            cancel="Cancel",
            target=self.on_confirm_remove_graph,
        )

        self._popups = (
            self._new_graph_popup,
            self._import_graph_popup,
            self._export_graph_popup,
            self._confirm_remove_graph_popup,
        )

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
        self._central_dock_id = dock_center_top = split_result.id_at_opposite_dir

        dock_window(self.flow_tree.get_window_name(), dock_left_top)
        dock_window(self.flow_graphs.get_window_name(), dock_left_bottom)
        dock_window(self.flow_dtypes.get_window_name(), dock_left_bottom)
        dock_window(self.flow_nodes.get_window_name(), dock_left_bottom)

        dock_window(self.flow_props.get_window_name(), dock_right_top)
        dock_window(self.flow_history.get_window_name(), dock_right_bottom)

        dock_window(self.flow_debug.get_window_name(), dock_center_bottom)
        dock_window(self.flow_logging.get_window_name(), dock_center_bottom)
        dock_window(self.flow_dtype.get_window_name(), dock_center_bottom)
        dock_window(self.flow_node.get_window_name(), dock_center_bottom)

        dock_window(self.dashboard.get_window_name(), dock_center_top)

        for tool_window in self._tools.values():
            tool_window.set_opened_window(True)

        for main_window in self._mains.values():
            main_window.set_opened_window(True)
            dock_window(main_window.get_window_name(), dock_center_top)

        # dock_left_top_node = imgui.internal.dock_builder_get_node(dock_left_top)
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_docking_split
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_resize
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_undocking

    def initialize_dock_layout(
        self,
        dockspace_id: int,
        viewport: imgui.Viewport,
        *,
        overwrite=False,
    ) -> None:
        if not enabled_docking_flag():
            return

        if self._initialized_dock_layout:
            return

        if overwrite:
            remove_node(dockspace_id)

        dock_node = get_node(dockspace_id)
        if not dock_node.is_empty():
            self._central_dock_id = dock_node.central_node.id_
            self._initialized_dock_layout = True
            return

        try:
            self._initialize_dock_layout(dockspace_id, viewport)
        finally:
            finish(dockspace_id)
            self._initialized_dock_layout = True

    @property
    def focused_key(self) -> str:
        return self._context.config.navigation.focused_key

    @focused_key.setter
    def focused_key(self, value: str) -> None:
        self._context.config.navigation.focused_key = value

    @property
    def focused_window(self):
        if focused_key := self.focused_key:
            return self._mains.get(focused_key)
        else:
            return None

    def on_new_graph(self, name: str) -> None:
        self.context.flows.create_graph(name=name, append=True, opened=True)

    def on_import_graph(self, file: str) -> None:
        pass

    def on_export_graph(self, file: str) -> None:
        pass

    def on_confirm_remove_graph(self, value: bool) -> None:
        pass

    def filter_window_key_set(self, cls: Type[WindowInterface]):
        return set(key for key, win in self._mains.items() if isinstance(win, cls))

    def sync_graph_windows(self) -> None:
        flow_graph_keys = set(self._context.flows.graphs.keys())
        graph_window_keys = self.filter_window_key_set(flow.GraphFlowWindow)
        if flow_graph_keys == graph_window_keys:
            return

        for remove_key in graph_window_keys - flow_graph_keys:
            self._mains.pop(remove_key)

        for create_key in flow_graph_keys - graph_window_keys:
            graph_windows = flow.GraphFlowWindow(self._context, GraphKey(create_key))
            self._mains[create_key] = graph_windows
            if self._central_dock_id is not None:
                dock_window(graph_windows.get_window_name(), self._central_dock_id)

    def sync_canvas_windows(self) -> None:
        flow_canvas_keys = set(self._context.canvases.keys())
        canvas_window_keys = self.filter_window_key_set(canvas.CanvasWindow)
        if flow_canvas_keys == canvas_window_keys:
            return

        for remove_key in canvas_window_keys - flow_canvas_keys:
            self._mains.pop(remove_key)

        for create_key in flow_canvas_keys - canvas_window_keys:
            canvas_windows = canvas.CanvasWindow(self._context, CanvasKey(create_key))
            self._mains[create_key] = canvas_windows
            if self._central_dock_id is not None:
                dock_window(canvas_windows.get_window_name(), self._central_dock_id)

    @override
    def on_main_menu(self) -> None:
        for name, func in self._prefix_menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

        if window := self.focused_window:
            window.on_main_menu()

        for name, func in self._suffix_menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    def on_file_menu(self) -> None:
        if menu_item("New graph"):
            self._new_graph_popup.show()

        imgui.separator()
        if imgui.begin_menu("Recent canvases"):
            try:
                for canvas_ in self.context.canvases.values():
                    if menu_item(f"{canvas_.name}###{canvas_.uuid}"):
                        self.focused_key = canvas_.uuid
                        canvas_.opened = True
            finally:
                imgui.end_menu()
        if imgui.begin_menu("Recent graphs"):
            try:
                for graph in self.context.flows.graphs.values():
                    if menu_item(f"{graph.name}###{graph.uuid}"):
                        self.focused_key = graph.uuid
                        graph.opened = True
            finally:
                imgui.end_menu()

        imgui.separator()
        if menu_item("Import graph"):
            self._import_graph_popup.show()

        if menu_item("Export graph", enabled=False):
            self._export_graph_popup.show()

        imgui.separator()
        if menu_item("Refresh canvas"):
            self.context.canvases.read_all_config_files()
        if menu_item("Refresh graphs"):
            self.context.flows.read_all_graph_files()

    def filter_tools_with_module(self, module: ModuleType):
        result = list()
        for tool in self._tools.values():
            if not tool.__module__.startswith(module.__name__):
                continue
            result.append(tool)
        return result

    def do_window_tool_menu(self, label: str, module: ModuleType):
        if imgui.begin_menu(label):
            try:
                tools = self.filter_tools_with_module(module)
                if menu_item("Show all"):
                    for tool in tools:
                        tool.set_opened_window(True)
                if menu_item("Hide all"):
                    for tool in tools:
                        tool.set_opened_window(False)

                imgui.separator()
                for tool in tools:
                    opened = tool.get_opened_window()
                    if opened is None:
                        continue
                    if menu_item(tool.get_window_name(), selected=opened):
                        tool.set_opened_window(not opened)
            finally:
                imgui.end_menu()

    def on_window_menu(self):
        self.do_window_tool_menu("Canvas", canvas)
        self.do_window_tool_menu("Flow", flow)

    @override
    def on_status_menu(self) -> None:
        if window := self.focused_window:
            window.on_status_menu()

    @override
    def do_event(self, event: Event) -> bool:
        if window := self.focused_window:
            return window.on_event(event)
        else:
            return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        if window := self.focused_window:
            return window.on_msg(msg)
        else:
            return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        if window := self.focused_window:
            window.on_keyboard(keys)

    @override
    def do_process(self) -> None:
        name = self.get_mode_name()
        viewport = imgui.get_main_viewport()
        with dockspace_over_viewport_context(name, viewport=viewport) as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id
            if not self._initialized_dock_layout:
                self.initialize_dock_layout(dockspace_id, viewport)

        self.sync_graph_windows()
        self.sync_canvas_windows()

        for tool_window in self._tools.values():
            tool_window.do_process()

        for main_window in self._mains.values():
            main_window.do_process()

        for popup in self._popups:
            popup.do_process()

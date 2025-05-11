# -*- coding: utf-8 -*-

from types import ModuleType
from typing import Dict, Final, List, NamedTuple, Optional, Type

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.apps.player.modes.main.position import DockPosition
from cvp.context.context import Context
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
from cvp.msgs.msg import Msg


class ModulesAndTools(NamedTuple):
    modules: List[ModuleType]
    tools: Dict[str, WindowInterface]


def create_tool_windows(context: Context) -> ModulesAndTools:
    from cvp.apps.player.modes.main import canvas, flow

    windows = list()
    windows.extend(canvas.create_canvas_tool_windows(context))
    windows.extend(flow.create_flow_tool_windows(context))

    modules = [canvas, flow]
    tools = {type(w).__name__: w for w in windows}
    return ModulesAndTools(modules, tools)


class MainLayout:
    _DOCKSPACE_NAME: Final[str] = "Main"

    _LEFT_RATIO: Final[float] = 0.15
    _RIGHT_RATIO: Final[float] = 0.15
    _LEFT_UP_RATIO: Final[float] = 0.60
    _RIGHT_UP_RATIO: Final[float] = 0.60
    _BOTTOM_RATIO: Final[float] = 0.25

    _central_dock_id: Optional[int]
    _modules: List[ModuleType]
    _tools: Dict[str, WindowInterface]
    _mains: Dict[str, WindowInterface]

    def __init__(self, context: Context):
        self._context = context
        self._initialized_dock_layout = False
        self._central_dock_id = None

        modules_tools = create_tool_windows(context)
        self._modules = modules_tools.modules
        self._tools = modules_tools.tools
        self._mains = dict()

    @property
    def context(self):
        return self._context

    @property
    def initialized(self):
        return self._initialized_dock_layout

    @property
    def tools(self):
        return self._tools

    @property
    def mains(self):
        return self._mains

    def add_main_window(self, key: str, window: WindowInterface) -> None:
        self._mains[key] = window
        if self._central_dock_id is not None:
            dock_window(window.get_window_name(), self._central_dock_id)

    def _initialize_dock_layout(
        self,
        dockspace_id: int,
        viewport: imgui.Viewport,
    ) -> int:
        remove_node(dockspace_id)
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

        def _get_docker_node_id(dock_position: DockPosition) -> int:
            match dock_position:
                case DockPosition.left_top:
                    return dock_left_top
                case DockPosition.left_bottom:
                    return dock_left_bottom
                case DockPosition.center_top:
                    return dock_center_top
                case DockPosition.center_bottom:
                    return dock_center_bottom
                case DockPosition.right_top:
                    return dock_right_top
                case DockPosition.right_bottom:
                    return dock_right_bottom
                case _:
                    assert False, "Inaccessible section"

        for tool_window in self._tools.values():
            tool_window.set_opened_window(True)
            dock_node_id = _get_docker_node_id(tool_window.get_window_position())
            dock_window(tool_window.get_window_name(), dock_node_id)

        for main_window in self._mains.values():
            assert main_window.get_window_position() == DockPosition.center_top
            main_window.set_opened_window(True)
            dock_window(main_window.get_window_name(), dock_center_top)

        # dock_left_top_node = imgui.internal.dock_builder_get_node(dock_left_top)
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_docking_split
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_resize
        # dock_left_top_node.local_flags |= imgui.DockNodeFlags_.no_undocking

        return dock_center_top

    def initialize_dock_layout(
        self,
        dockspace_id: int,
        viewport: imgui.Viewport,
    ) -> None:
        if not enabled_docking_flag():
            return

        if self._initialized_dock_layout:
            return

        dock_node = get_node(dockspace_id)
        if not dock_node.is_empty():
            self._central_dock_id = dock_node.central_node.id_
            self._initialized_dock_layout = True
            return

        try:
            self._central_dock_id = self._initialize_dock_layout(dockspace_id, viewport)
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

    def filter_window_key_set(self, cls: Type[WindowInterface]):
        return set(key for key, win in self._mains.items() if isinstance(win, cls))

    @staticmethod
    def filter_windows_with_module(
        windows: Dict[str, WindowInterface],
        module: ModuleType,
    ):
        result = dict()
        for key, window in windows.items():
            if not window.__module__.startswith(module.__name__):
                continue
            result[key] = window
        return result

    def filter_tools_with_module(self, module: ModuleType):
        assert module in self._modules
        return self.filter_windows_with_module(self._tools, module)

    def filter_mains_with_module(self, module: ModuleType):
        assert module in self._modules
        return self.filter_windows_with_module(self._mains, module)

    def do_main_menu(self) -> None:
        if window := self.focused_window:
            window.on_main_menu()

    def do_window_menu(self, label: str, module: ModuleType) -> None:
        assert module in self._modules
        if imgui.begin_menu(label):
            try:
                tools = self.filter_tools_with_module(module)

                for tool in tools.values():
                    opened = tool.get_opened_window()
                    if opened is None:
                        continue
                    if menu_item(tool.get_window_name(), selected=opened):
                        tool.set_opened_window(not opened)

                imgui.separator()
                if menu_item("Show all"):
                    for tool in tools.values():
                        tool.set_opened_window(True)
                if menu_item("Hide all"):
                    for tool in tools.values():
                        tool.set_opened_window(False)
            finally:
                imgui.end_menu()

    def do_status_menu(self) -> None:
        if window := self.focused_window:
            window.on_status_menu()

    def do_event(self, event: Event) -> bool:
        if window := self.focused_window:
            return window.on_event(event)
        else:
            return False

    def do_msg(self, msg: Msg) -> bool:
        if window := self.focused_window:
            return window.on_msg(msg)
        else:
            return False

    def do_keyboard(self, keys: ScancodeWrapper) -> None:
        if window := self.focused_window:
            window.on_keyboard(keys)

    def do_dockspace_process(self) -> None:
        viewport = imgui.get_main_viewport()
        with dockspace_over_viewport_context(
            self._DOCKSPACE_NAME,
            viewport=viewport,
        ) as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id
            if not self._initialized_dock_layout:
                self.initialize_dock_layout(dockspace_id, viewport)

    def do_process(self, module: ModuleType) -> None:
        assert module in self._modules
        for tool in self.filter_tools_with_module(module).values():
            tool.on_process()
        for main in self.filter_mains_with_module(module).values():
            main.on_process()

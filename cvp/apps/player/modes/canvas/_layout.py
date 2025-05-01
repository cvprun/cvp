# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence, Union

from imgui_bundle import imgui

from cvp.apps.player.modes.canvas._base import CanvasWindowInterface
from cvp.apps.player.windows.canvas import CanvasWindow
from cvp.canvas.canvas import CanvasKey
from cvp.context.context import Context
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


class CanvasLayout:
    _LEFT_RATIO: Final[float] = 0.15
    _RIGHT_RATIO: Final[float] = 0.15
    _LEFT_UP_RATIO: Final[float] = 0.60
    _RIGHT_UP_RATIO: Final[float] = 0.60
    _BOTTOM_RATIO: Final[float] = 0.25

    _windows: Sequence[CanvasWindowInterface]
    _main_dock_id: Optional[int]

    def __init__(self, context: Context):
        from cvp.apps.player.modes.canvas.history import HistoryCanvasWindow
        from cvp.apps.player.modes.canvas.intro import IntroCanvasWindow
        from cvp.apps.player.modes.canvas.layers import LayersCanvasWindow
        from cvp.apps.player.modes.canvas.options import OptionsCanvasWindow
        from cvp.apps.player.modes.canvas.timeline import TimelineCanvasWindow
        from cvp.apps.player.modes.canvas.tools import ToolsCanvasWindow

        self._context = context
        self._initialized_dock_layout = False
        self._main_dock_id = None

        self.history = HistoryCanvasWindow(context)
        self.intro = IntroCanvasWindow(context)
        self.layers = LayersCanvasWindow(context)
        self.options = OptionsCanvasWindow(context)
        self.timeline = TimelineCanvasWindow(context)
        self.tools = ToolsCanvasWindow(context)

        self._windows = (
            # Left Dock
            self.tools,
            self.options,
            # Right Dock
            self.history,
            self.layers,
            # Bottom Dock
            self.timeline,
            # Main Dock
            self.intro,
        )

        self._canvas_windows = CanvasWindow.create_opened_windows(context)

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

        dock_window(self.tools.get_window_name(), dock_left_top)
        dock_window(self.options.get_window_name(), dock_left_bottom)

        dock_window(self.history.get_window_name(), dock_right_top)
        dock_window(self.layers.get_window_name(), dock_right_bottom)

        dock_window(self.timeline.get_window_name(), dock_center_bottom)

        dock_window(self.intro.get_window_name(), dock_center_top)
        for cw in self._canvas_windows.values():
            dock_window(cw.get_window_name(), dock_center_top)
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
        if focused_key := self._context.canvases.focused_key:
            return self._canvas_windows.get(focused_key)
        else:
            return None

    def refresh_canvas(self, *, raise_errors=False) -> None:
        prev_keys = set(self._canvas_windows.keys())
        self._canvas_windows.clear()

        # -----------------------------------------
        self._context.canvases.clear()
        self._context.canvases.read_all_config_files(raise_errors=raise_errors)
        # -----------------------------------------

        self._canvas_windows = CanvasWindow.create_opened_windows(self._context)
        for cw_key, cw in self._canvas_windows.items():
            if self._main_dock_id is not None and cw_key not in prev_keys:
                dock_window(cw.get_window_name(), self._main_dock_id)

    def create_canvas_window(self, key: CanvasKey):
        canvas_windows = CanvasWindow(self._context, key)
        self._canvas_windows[key] = canvas_windows
        if self._main_dock_id is not None:
            dock_window(canvas_windows.get_window_name(), self._main_dock_id)
        return canvas_windows

    def remove_canvas_window(self, key: CanvasKey):
        return self._canvas_windows.pop(key)

    def sync_canvas_windows(self) -> None:
        canvas_keys = set(self._context.canvases.keys())
        window_keys = set(self._canvas_windows.keys())
        if canvas_keys == window_keys:
            return

        for remove_key in window_keys - canvas_keys:
            self.remove_canvas_window(remove_key)

        for create_key in canvas_keys - window_keys:
            self.create_canvas_window(create_key)

        canvas_keys = set(self._context.canvases.keys())
        window_keys = set(self._canvas_windows.keys())
        assert canvas_keys == window_keys

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

        self.sync_canvas_windows()

        focused_window = self.focused_window
        for window in self._windows:
            window.do_process(focused_window)

        for cw in self._canvas_windows.values():
            cw.do_process()

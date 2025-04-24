# -*- coding: utf-8 -*-

from typing import Callable, Sequence, Tuple

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.flow._layout import _FlowLayout
from cvp.context.context import Context
from cvp.fonts.glyphs import mdi
from cvp.imgui.dockspace import dockspace_over_viewport_context
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.menu_item_ex import menu_item
from cvp.msgs.msg import Msg
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_number__ = 3
    __cvp_mode_name__ = "Flow"

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = _FlowLayout()
        self._windows = self._layout.create_windows(context)
        self._viewport_flags = ROOT_STATIC_VIEWPORT_FLAGS
        self._initialized_dock_layout = False
        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
            ("Run", self.on_run_menu),
            ("Deploy", self.on_deploy_menu),
            ("View", self.on_view_menu),
        )

    @property
    def config(self):
        return self.context.config.flow_aui

    @property
    def show_layout(self) -> bool:
        return self.config.nodes.show_layout

    @show_layout.setter
    def show_layout(self, value: bool) -> None:
        self.config.nodes.show_layout = value

    @property
    def autoscroll(self) -> bool:
        return self.config.logs.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.config.logs.autoscroll = value

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    def on_file_menu(self) -> None:
        pass

    def on_edit_menu(self) -> None:
        self._process_disabled_edit_menu()

    def on_layer_menu(self) -> None:
        self._process_disabled_layer_menu()
        imgui.separator()
        self._process_disabled_align_menu()
        self._process_disabled_distribute_menu()

    def on_run_menu(self) -> None:
        self._process_disabled_run_menu()

    def on_deploy_menu(self) -> None:
        self._process_disabled_deploy_menu()

    def on_view_menu(self) -> None:
        if autoscroll := menu_item("Autoscroll logs", selected=self.autoscroll):
            self.autoscroll = autoscroll.state

        imgui.separator()
        if show_layout := menu_item("Show Layout", selected=self.show_layout):
            self.show_layout = show_layout.state

    @staticmethod
    def _process_disabled_edit_menu() -> None:
        menu_item("Undo", shortcut="Ctrl+Z", enabled=False)
        menu_item("Redo", shortcut="Ctrl+Y", enabled=False)
        imgui.separator()
        menu_item("Cut", shortcut="Ctrl+X", enabled=False)
        menu_item("Copy", shortcut="Ctrl+C", enabled=False)
        menu_item("Paste", shortcut="Ctrl+V", enabled=False)
        imgui.separator()
        menu_item("Delete", shortcut="Del", enabled=False)
        imgui.separator()
        menu_item("Reset control", enabled=False)
        imgui.separator()
        menu_item("Select all", enabled=False)
        menu_item("Select nodes", enabled=False)
        menu_item("Select wires", enabled=False)
        menu_item("Select pins", enabled=False)

    @staticmethod
    def _process_disabled_layer_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    @staticmethod
    def _process_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    @staticmethod
    def _process_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    @staticmethod
    def _process_disabled_run_menu() -> None:
        imgui.begin_menu(f"{mdi.PLAY} Run", enabled=False)
        imgui.begin_menu(f"{mdi.BUG} Debug", enabled=False)
        imgui.separator()
        menu_item(f"{mdi.PAUSE} Pause", enabled=False)
        menu_item(f"{mdi.STOP} Stop", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OVER} Step Over", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_INTO} Step Into", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OUT} Step Out", enabled=False)

    @staticmethod
    def _process_disabled_deploy_menu() -> None:
        menu_item("Upload to ...", enabled=False)

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @override
    def do_process(self) -> None:
        viewport = imgui.get_main_viewport()
        with dockspace_over_viewport_context(viewport=viewport) as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id
            if not self._layout.initialized:
                self._layout.initialize_dock_layout(dockspace_id, viewport)

        for window in self._windows.values():
            window.do_process()

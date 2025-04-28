# -*- coding: utf-8 -*-

from pathlib import Path
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
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_number__ = 3
    __cvp_mode_name__ = "Flow"

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = _FlowLayout(context)
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

        self._open_workspace_popup = OpenFilePopup(
            title="Open workspace",
            target=self.on_open_workspace_popup,
        )
        self._import_workspace_popup = OpenFilePopup(
            title="Import workspace",
            target=self.on_import_workspace,
        )
        self._export_workspace_popup = OpenFilePopup(
            title="Export workspace",
            target=self.on_export_workspace,
        )
        self._confirm_remove_workspace_popup = ConfirmPopup(
            title="Remove workspace",
            label="Are you sure you want to remove workspace?",
            ok="Remove",
            cancel="Cancel",
            target=self.on_confirm_remove_workspace,
        )
        self._new_variable_popup = InputTextPopup(
            title="New variable",
            label="Please enter a variable name:",
            ok="Add",
            cancel="Cancel",
            target=self.on_new_variable,
        )

        self._popups = (
            self._open_workspace_popup,
            self._import_workspace_popup,
            self._export_workspace_popup,
            self._confirm_remove_workspace_popup,
            self._new_variable_popup,
        )

    def on_new_graph(self, name: str) -> None:
        # graph = self.flows.create_graph(name, append=True)
        # filepath = self.context.home.flows.graph_filepath(graph.key)
        # if filepath.exists():
        #     raise FileExistsError(f"Graph file already exists: '{str(filepath)}'")
        # self.flows.write_graph_yaml(filepath, graph)
        # self._canvases.open(graph)
        pass

    def on_open_workspace_popup(self, file: str) -> None:
        if not file:
            return

        path = Path(file)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        if not path.is_dir():
            raise NotADirectoryError(f"'{file}' is not a directory")

        self.context.open_flow_workspace(path)

    def on_import_workspace(self, file: str) -> None:
        pass

    def on_export_workspace(self, file: str) -> None:
        pass

    def on_confirm_remove_workspace(self, value: bool) -> None:
        pass

    def on_new_variable(self, name: str) -> None:
        # if not name:
        #     raise ValueError("Variable name cannot be empty")
        # canvas = self._canvases.canvas
        # if canvas is None:
        #     raise ValueError("Canvas cannot be none")
        # with canvas:
        #     canvas.graph.add_variable(name, self._drag_dtype)
        pass

    @property
    def config(self):
        return self.context.config.flow

    @property
    def flows(self):
        return self.context.flows

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
        if menu_item("New workspace"):
            self._open_workspace_popup.show()
            pass

        if menu_item("Open workspace"):
            pass

        recent_items = self.context.get_flow_workspace_recent_items()
        has_any_recent = bool(recent_items)
        if imgui.begin_menu("Recent workspace", enabled=has_any_recent):
            try:
                for recent in recent_items:
                    if menu_item(recent.name):
                        self.context.open_flow_workspace(recent.path)
            finally:
                imgui.end_menu()

        imgui.separator()
        # has_opened_graph = self._canvases.opened
        # if menu_item("Save graph", enabled=has_opened_graph):
        #     self.save_current_graph()
        # if menu_item("Save and close graph", enabled=has_opened_graph):
        #     self.save_current_graph()
        #     self.close_current_graph()
        # if menu_item("Close graph", enabled=has_opened_graph):
        #     self.close_current_graph()

        imgui.separator()
        if menu_item("Import graph"):
            # self._import_graph_popup.show()
            pass
        if menu_item("Export graph"):
            # self._export_graph_popup.show()
            pass

        imgui.separator()
        if menu_item("Refresh graphs"):
            # self.context.flows.workspaces.read_all_config_files()
            pass

        imgui.separator()
        if menu_item("Close workspace", enabled=self.context.opened_flow_workspace()):
            self.context.close_flow_workspace()
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

        self._layout.do_process()

        for popup in self._popups:
            popup.do_process()

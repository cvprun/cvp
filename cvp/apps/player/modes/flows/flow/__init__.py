# -*- coding: utf-8 -*-

from typing import Callable, Sequence, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.flows.flow._layout import FlowLayout
from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_number__ = 3
    __cvp_mode_name__ = "Flow"

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = FlowLayout(context)
        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
            ("Run", self.on_run_menu),
            ("Deploy", self.on_deploy_menu),
            ("View", self.on_view_menu),
        )

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

        # self._new_variable_popup = InputTextPopup(
        #     title="New variable",
        #     label="Please enter a variable name:",
        #     ok="Add",
        #     cancel="Cancel",
        #     target=self.on_new_variable,
        # )

        self._popups = (
            self._new_graph_popup,
            self._import_graph_popup,
            self._export_graph_popup,
            self._confirm_remove_graph_popup,
            # self._new_variable_popup,
        )

    def on_new_graph(self, name: str) -> None:
        self.context.flows.create_graph(name=name, append=True, opened=True)

    def on_import_graph(self, file: str) -> None:
        pass

    def on_export_graph(self, file: str) -> None:
        pass

    def on_confirm_remove_graph(self, value: bool) -> None:
        pass

    # def on_new_variable(self, name: str) -> None:
    #     if not name:
    #         raise ValueError("Variable name cannot be empty")
    #     canvas = self._canvases.canvas
    #     if canvas is None:
    #         raise ValueError("Canvas cannot be none")
    #     with canvas:
    #         canvas.graph.add_variable(name, self._drag_dtype)

    @property
    def config(self):
        return self.context.config.flow

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
        if menu_item("New Graph"):
            self._new_graph_popup.show()

        # imgui.separator()
        # recent_items = self.context.get_flow_graph_recent_items()
        # has_any_recent = bool(recent_items)
        # if imgui.begin_menu("Recent graph", enabled=has_any_recent):
        #     try:
        #         for recent in recent_items:
        #             if menu_item(recent.value):
        #                 self.context.open_flow_graph(recent.value)
        #     finally:
        #         imgui.end_menu()

        imgui.separator()
        focused_window = self._layout.focused_window
        if focused_window is not None:
            focused_window.do_file_menu()
        else:
            self.do_disabled_file_menu()

        imgui.separator()
        has_focused = bool(focused_window)
        if menu_item("Import graph"):
            self._import_graph_popup.show()
        if menu_item("Export graph", enabled=has_focused):
            self._export_graph_popup.show()

        imgui.separator()
        if menu_item("Refresh graphs"):
            self.context.flows.read_all_graph_files()

    def on_edit_menu(self) -> None:
        if window := self._layout.focused_window:
            window.do_edit_menu()
        else:
            self.do_disabled_edit_menu()

    def on_layer_menu(self) -> None:
        if window := self._layout.focused_window:
            window.do_layer_menu()
            imgui.separator()
            window.do_align_menu()
            window.do_distribute_menu()
        else:
            self.do_disabled_layer_menu()
            imgui.separator()
            self.do_disabled_align_menu()
            self.do_disabled_distribute_menu()

    def on_run_menu(self) -> None:
        if window := self._layout.focused_window:
            window.do_run_menu()
        else:
            self.do_disabled_run_menu()

    def on_deploy_menu(self) -> None:
        if window := self._layout.focused_window:
            window.do_deploy_menu()
        else:
            self.do_disabled_deploy_menu()

    def on_view_menu(self) -> None:
        if autoscroll := menu_item("Autoscroll logs", selected=self.autoscroll):
            self.autoscroll = autoscroll.state
        imgui.separator()
        if show_layout := menu_item("Show Layout", selected=self.show_layout):
            self.show_layout = show_layout.state

    @staticmethod
    def do_disabled_file_menu() -> None:
        menu_item("Save graph", enabled=False)
        menu_item("Save and close graph", enabled=False)
        menu_item("Force close graph", enabled=False)

    @staticmethod
    def do_disabled_edit_menu() -> None:
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
    def do_disabled_layer_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    @staticmethod
    def do_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    @staticmethod
    def do_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    @staticmethod
    def do_disabled_run_menu() -> None:
        imgui.begin_menu(f"{mdi.PLAY} Run", enabled=False)
        imgui.begin_menu(f"{mdi.BUG} Debug", enabled=False)
        imgui.separator()
        menu_item(f"{mdi.PAUSE} Pause", enabled=False)
        menu_item(f"{mdi.STOP} Stop", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OVER} Step Over", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_INTO} Step Into", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OUT} Step Out", enabled=False)

    @staticmethod
    def do_disabled_deploy_menu() -> None:
        menu_item("Upload to ...", enabled=False)

    @override
    def do_process(self) -> None:
        self._layout.do_process()

        for popup in self._popups:
            popup.do_process()

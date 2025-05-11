# -*- coding: utf-8 -*-

from typing import Set

from imgui_bundle import imgui

from cvp.apps.player.modes.main import flow
from cvp.apps.player.modes.main.base_main import BaseMainMode
from cvp.apps.player.modes.main.flow.graph import GraphFlowWindow
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.apps.player.modes.main.layout import MainLayout
from cvp.flow.graph import GraphKey
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class FlowMode(BaseMainMode):
    __cvp_mode_name__ = "Flow"

    def __init__(self, layout: MainLayout):
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

        menus = (("File", self.on_file_menu),)
        popups = (
            self._new_graph_popup,
            self._import_graph_popup,
            self._export_graph_popup,
            self._confirm_remove_graph_popup,
        )

        super().__init__(
            layout=layout,
            module=flow,
            main_window_type=GraphFlowWindow,
            menus=menus,
            popups=popups,
        )

    def on_new_graph(self, name: str) -> None:
        self.context.flows.create_graph(name=name, append=True, opened=True)

    def on_import_graph(self, file: str) -> None:
        pass

    def on_export_graph(self, file: str) -> None:
        pass

    def on_confirm_remove_graph(self, value: bool) -> None:
        pass

    def on_file_menu(self) -> None:
        if menu_item("New graph"):
            self._new_graph_popup.show()

        imgui.separator()
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

    @override
    def get_main_key_set(self) -> Set[str]:
        return set(self._context.flows.graphs.keys())

    @override
    def on_window_popped(self, window: WindowInterface) -> None:
        assert isinstance(window, GraphFlowWindow)

    @override
    def on_window_creation(self, key: str) -> WindowInterface:
        return GraphFlowWindow(self.context, GraphKey(key))

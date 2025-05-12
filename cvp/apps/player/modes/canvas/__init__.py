# -*- coding: utf-8 -*-

from typing import Set

from imgui_bundle import imgui

from cvp.apps.player.modes.main import canvas as canvas_module
from cvp.apps.player.modes.main.base_main import BaseMainMode
from cvp.apps.player.modes.main.canvas.canvas import CanvasWindow
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.apps.player.modes.main.layout import MainLayout
from cvp.assets.fonts.mdi import DRAWING
from cvp.canvas.canvas import CanvasKey
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class CanvasMode(BaseMainMode):
    __cvp_mode_name__ = "Canvas"
    __cvp_mode_icon__ = DRAWING

    def __init__(self, layout: MainLayout):
        self._new_canvas_popup = InputTextPopup(
            title="New canvas",
            label="Please enter a canvas name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_canvas,
        )
        self._import_canvas_popup = OpenFilePopup(
            title="Import canvas",
            target=self.on_import_canvas,
        )
        self._export_canvas_popup = OpenFilePopup(
            title="Export canvas",
            target=self.on_export_canvas,
            open_mode=OpenFilePopup.OpenMode.input_filename,
        )
        self._confirm_remove_canvas_popup = ConfirmPopup(
            title="Remove canvas",
            label="Are you sure you want to remove canvas?",
            ok="Remove",
            cancel="Cancel",
            target=self.on_confirm_remove_canvas,
        )

        menus = (("File", self.on_file_menu),)
        popups = (
            self._new_canvas_popup,
            self._import_canvas_popup,
            self._export_canvas_popup,
            self._confirm_remove_canvas_popup,
        )

        super().__init__(
            layout=layout,
            module=canvas_module,
            main_window_type=CanvasWindow,
            menus=menus,
            popups=popups,
        )

    def on_new_canvas(self, name: str) -> None:
        pass

    def on_import_canvas(self, file: str) -> None:
        pass

    def on_export_canvas(self, file: str) -> None:
        pass

    def on_confirm_remove_canvas(self, value: bool) -> None:
        pass

    def on_file_menu(self) -> None:
        if menu_item("New canvas"):
            self._new_canvas_popup.show()

        imgui.separator()
        if imgui.begin_menu("Recent canvases"):
            try:
                for canvas in self.context.canvases.values():
                    if menu_item(f"{canvas.name}###{canvas.key}"):
                        self.context.selected_canvas_key = canvas.key
                        canvas.opened = True
            finally:
                imgui.end_menu()

        imgui.separator()
        if menu_item("Import canvas"):
            self._import_canvas_popup.show()
        if menu_item("Export canvas", enabled=False):
            self._export_canvas_popup.show()

        imgui.separator()
        if menu_item("Refresh canvas"):
            self.context.canvases.read_all_config_files()

    @override
    def get_selected_main_key(self) -> str:
        return self.context.selected_canvas_key

    @override
    def get_main_key_set(self) -> Set[str]:
        return set(self.context.canvases.keys())

    @override
    def on_window_popped(self, window: WindowInterface) -> None:
        assert isinstance(window, CanvasWindow)

    @override
    def on_window_creation(self, key: str) -> WindowInterface:
        return CanvasWindow(self.context, CanvasKey(key))

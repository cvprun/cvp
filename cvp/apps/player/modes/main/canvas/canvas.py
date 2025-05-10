# -*- coding: utf-8 -*-

from typing import Callable, Sequence, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.main._main import MainWindow
from cvp.canvas.canvas import CanvasKey
from cvp.context.context import Context
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas
from cvp.types.override import override


class CanvasWindow(ControllableCanvas, MainWindow):
    __cvp_window_name__ = "Canvas"

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context, canvas_key: CanvasKey):
        ControllableCanvas.__init__(self)
        MainWindow.__init__(self, context)
        self._canvas_key = canvas_key

        canvas = context.canvases[canvas_key]
        self._pan_x.update(canvas.control.pan_x, no_emit=True)
        self._pan_y.update(canvas.control.pan_y, no_emit=True)
        self._zoom.update(canvas.control.zoom, no_emit=True)

        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
            ("View", self.on_view_menu),
        )

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
        self._popups = (
            self._new_canvas_popup,
            self._import_canvas_popup,
            self._export_canvas_popup,
            self._confirm_remove_canvas_popup,
        )

    @classmethod
    def create_opened_windows(cls, context: Context):
        result = dict()
        for key, canvas in context.canvases.items():
            if not canvas.opened:
                continue
            result[key] = cls(context, key)
        return result

    def on_new_canvas(self, name: str) -> None:
        pass

    def on_import_canvas(self, file: str) -> None:
        pass

    def on_export_canvas(self, file: str) -> None:
        pass

    def on_confirm_remove_canvas(self, value: bool) -> None:
        pass

    @property
    def canvas_key(self):
        return self._canvas_key

    @property
    def canvas(self):
        return self.context.canvases[self._canvas_key]

    @property
    def focused_key(self):
        return CanvasKey(self.context.config.navigation.focused_key)

    @focused_key.setter
    def focused_key(self, value: CanvasKey) -> None:
        self.context.config.navigation.focused_key = str(value)

    @property
    def has_focused_key(self):
        return self.context.config.navigation.focused_key == self._canvas_key

    @property
    def config(self):
        return self.context.config.canvas

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text()

    @override
    def get_window_name(self) -> str:
        window_name = self.__cvp_window_name__
        canvas = self.context.flows.canvass.get(self._canvas_key)
        canvas_name = canvas.name if canvas else window_name
        return f"{canvas_name}###{window_name}/{self._canvas_key}"

    @override
    def do_process(self) -> None:
        pass

    # ==================================================================================
    # region: Context Menu Operations
    # ==================================================================================

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    def on_file_menu(self) -> None:
        if menu_item("New canvas"):
            pass

        imgui.separator()
        if self.has_focused_key:
            self.do_file_menu()
        else:
            self.do_disabled_file_menu()

        imgui.separator()
        if menu_item("Import canvas"):
            pass
        if menu_item("Export canvas", enabled=self.has_focused_key):
            pass

    def on_edit_menu(self) -> None:
        if self.has_focused_key:
            self.do_edit_menu()
        else:
            self.do_disabled_edit_menu()

    def on_layer_menu(self) -> None:
        if self.has_focused_key:
            self.do_layer_menu()
            imgui.separator()
            self.do_align_menu()
            self.do_distribute_menu()
        else:
            self.do_disabled_layer_menu()
            imgui.separator()
            self.do_disabled_align_menu()
            self.do_disabled_distribute_menu()

    def on_view_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_file_menu() -> None:
        menu_item("Save canvas", enabled=False)
        menu_item("Save and close canvas", enabled=False)
        menu_item("Force close canvas", enabled=False)

    def do_file_menu(self) -> None:
        pass

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

    def do_edit_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_layer_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    def do_layer_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    def do_align_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    def do_distribute_menu(self) -> None:
        pass

    # ==================================================================================
    # endregion: Context Menu Operations
    # ==================================================================================

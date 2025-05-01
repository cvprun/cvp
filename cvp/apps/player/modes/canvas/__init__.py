# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.canvas._layout import CanvasLayout
from cvp.context.context import Context
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class CanvasMode(BaseMode):
    __cvp_mode_name__ = "Canvas"

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = CanvasLayout(context)
        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
        )

        self._open_image_popup = OpenFilePopup(
            title="Open image",
            target=self.on_open_image,
        )

        self._popups = (self._open_image_popup,)

    def on_open_image(self, file: str) -> None:
        pass

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    def on_file_menu(self) -> None:
        focused_window = self._layout.focused_window
        if focused_window is not None:
            focused_window.do_file_menu()
        else:
            self.do_disabled_file_menu()

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

    @staticmethod
    def do_disabled_file_menu() -> None:
        menu_item("Save canvas", enabled=False)
        menu_item("Save and close canvas", enabled=False)
        menu_item("Force close canvas", enabled=False)

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

    @override
    def do_process(self) -> None:
        self._layout.do_process()
        for popup in self._popups:
            popup.do_process()

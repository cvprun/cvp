# -*- coding: utf-8 -*-

from typing import Final, Optional, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.system._base import BaseSystem, SystemInterface
from cvp.apps.player.modes.system._manager import create_system_widgets
from cvp.assets.fonts.mdi import MONITOR_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class SystemMode(BaseMode):
    __cvp_mode_name__ = "System"
    __cvp_mode_icon__ = MONITOR_EYE

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._menus = create_system_widgets(context)

    def get_menu(self, name: str):
        return self._menus.get(name)

    def get_menu_with_type(self, cls: Type[SystemInterface]):
        return self.get_menu(cls.get_menu_name())

    @override
    def on_process(self) -> None:
        widget = self._menus.get(self.selected_submenu)
        if widget is not None:
            widget.on_preprocess()
        try:
            with self.begin_mode_context():
                self.do_child_process(widget)
        finally:
            if widget is not None:
                widget.on_postprocess()

    def do_child_process(self, widget: Optional[BaseSystem] = None) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    for key, menu in self._menus.items():
                        name = menu.get_menu_name()
                        icon = menu.get_menu_icon()
                        label = f"{icon} {name}"
                        if imgui.selectable(label, key == self.selected_submenu)[1]:
                            self.selected_submenu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if widget is not None:
                imgui.text(self.selected_submenu)
                imgui.separator()
                widget.on_process()
            else:
                text_centered("Please select a item")

    # def on_child_process(self) -> None:
    #     if imgui.begin_table("Table", len(self._headers), self._TABLE_FLAGS):
    #         try:
    #             for header in self._headers.values():
    #                 imgui.table_setup_column(header)
    #             imgui.table_headers_row()
    #
    #             for proc in self._infos.get().values():
    #                 imgui.table_next_row()
    #                 for i, key in enumerate(self._headers.keys()):
    #                     imgui.table_set_column_index(i)
    #                     imgui.text(str(getattr(proc, key)))
    #         finally:
    #             imgui.end_table()

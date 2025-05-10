# -*- coding: utf-8 -*-

from typing import Final, Optional, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.preference._base import BasePreference, PreferenceInterface
from cvp.apps.player.modes.preference._manager import create_preference_widgets
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class PreferenceMode(BaseMode):
    __cvp_mode_name__ = "Preference"

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._menus = create_preference_widgets(context)

    def get_menu(self, name: str):
        return self._menus.get(name)

    def get_menu_with_type(self, cls: Type[PreferenceInterface]):
        return self.get_menu(cls.get_menu_name())

    @property
    def layout_menu(self):
        # Lazy loading is intentional. Avoid 'circular import' issues.
        from cvp.apps.player.modes.preference.layout import LayoutPreference

        menu = self.get_menu_with_type(LayoutPreference)
        assert menu is not None
        assert isinstance(menu, LayoutPreference)
        return menu

    @override
    def do_process(self) -> None:
        widget = self._menus.get(self.selected_submenu)
        if widget is not None:
            widget.do_preprocess()
        try:
            with self.begin_mode_context():
                self.do_child_process(widget)
        finally:
            if widget is not None:
                widget.do_postprocess()

    def do_child_process(self, widget: Optional[BasePreference] = None) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected_submenu)[1]:
                            self.selected_submenu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if widget is not None:
                imgui.text(self.selected_submenu)
                imgui.separator()
                widget.do_process()
            else:
                text_centered("Please select a item")

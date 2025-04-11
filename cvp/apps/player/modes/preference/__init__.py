# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.preference._base import BasePreference
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import Context
from cvp.types.override import override
from cvp.variables import SIDE_MENU_WIDTH


@lru_cache
def create_preference_widget_types() -> Sequence[Type[BasePreference]]:
    from cvp.apps.player.modes.preference.appearance import AppearancePreference
    from cvp.apps.player.modes.preference.chat import ChatPreference
    from cvp.apps.player.modes.preference.keyring import KeyringPreference
    from cvp.apps.player.modes.preference.ollama import OllamaPreference
    from cvp.apps.player.modes.preference.resource import ResourcePreference
    from cvp.apps.player.modes.preference.supabase import SupabasePreference
    from cvp.apps.player.modes.preference.toast import ToastPreference

    return (
        AppearancePreference,
        ChatPreference,
        KeyringPreference,
        OllamaPreference,
        ResourcePreference,
        SupabasePreference,
        ToastPreference,
    )


def create_preference_widgets(context: Context):
    widget_types = create_preference_widget_types()
    return OrderedDict({wt.get_menu_name(): wt(context) for wt in widget_types})


class PreferenceMode(BaseMode):
    def __init__(self, context: Context):
        super().__init__(context)
        self._menus = create_preference_widgets(context)

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.preference

    @property
    def selected_menu(self) -> str:
        return self.context.config.preference_manager.selected_menu

    @selected_menu.setter
    def selected_menu(self, value: str) -> None:
        self.context.config.preference_manager.selected_menu = value

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(self):
        width = SIDE_MENU_WIDTH
        child_flags = RESIZE_X | BORDERS

        with begin_child_context("Menu", width, child_flags=child_flags):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected_menu)[1]:
                            self.selected_menu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if widget := self._menus.get(self.selected_menu):
                imgui.text(self.selected_menu)
                imgui.separator()
                widget.do_process()
            else:
                text_centered("Please select a item")

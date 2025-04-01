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
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import Context
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_MAIN_LABEL,
    DEFAULT_MENU_LABEL,
    DEFAULT_MENU_WIDTH,
    FULL_SIZE,
)


@lru_cache
def create_preference_widget_types() -> Sequence[Type[BasePreference]]:
    from cvp.apps.player.modes.preference.appearance import Appearance
    from cvp.apps.player.modes.preference.keyring import Keyring
    from cvp.apps.player.modes.preference.ollama import Ollama
    from cvp.apps.player.modes.preference.resource import Resource
    from cvp.apps.player.modes.preference.supabase import Supabase

    return (
        Appearance,
        Keyring,
        Ollama,
        Resource,
        Supabase,
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
    def selected(self) -> str:
        return self.context.config.preference_manager.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.context.config.preference_manager.selected = value

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        menu_label=DEFAULT_MENU_LABEL,
        main_label=DEFAULT_MAIN_LABEL,
        split_x=DEFAULT_MENU_WIDTH,
    ):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", FULL_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            if widget := self._menus.get(self.selected):
                imgui.text(self.selected)
                imgui.separator()
                widget.do_process()
            else:
                text_centered("Please select a item")

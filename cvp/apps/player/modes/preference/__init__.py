# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Optional, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.preference._base import BasePreference
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
    from cvp.apps.player.modes.preference.concurrency import ConcurrencyPreference
    from cvp.apps.player.modes.preference.developer import DeveloperPreference
    from cvp.apps.player.modes.preference.dtype import DtypePreference
    from cvp.apps.player.modes.preference.flow import FlowPreference
    from cvp.apps.player.modes.preference.font import FontPreference
    from cvp.apps.player.modes.preference.keyring import KeyringPreference
    from cvp.apps.player.modes.preference.layout import LayoutPreference
    from cvp.apps.player.modes.preference.logging import LoggingPreference
    from cvp.apps.player.modes.preference.node import NodePreference
    from cvp.apps.player.modes.preference.ollama import OllamaPreference
    from cvp.apps.player.modes.preference.overlay import OverlayPreference
    from cvp.apps.player.modes.preference.resource import ResourcePreference
    from cvp.apps.player.modes.preference.supabase import SupabasePreference
    from cvp.apps.player.modes.preference.toast import ToastPreference
    from cvp.apps.player.modes.preference.wsdl import WsdlPreference

    return (
        AppearancePreference,
        ConcurrencyPreference,
        DeveloperPreference,
        DtypePreference,
        FlowPreference,
        FontPreference,
        KeyringPreference,
        LayoutPreference,
        LoggingPreference,
        NodePreference,
        OllamaPreference,
        OverlayPreference,
        ResourcePreference,
        SupabasePreference,
        ToastPreference,
        WsdlPreference,
    )


def create_preference_widgets(context: Context):
    widget_types = create_preference_widget_types()
    return OrderedDict({wt.get_menu_name(): wt(context) for wt in widget_types})


class PreferenceMode(BaseMode):
    __cvp_mode_name__ = "Preference"

    def __init__(self, context: Context):
        super().__init__(context)
        self._menus = create_preference_widgets(context)

    @property
    def selected_menu(self) -> str:
        return self.context.config.preference_manager.selected_menu

    @selected_menu.setter
    def selected_menu(self, value: str) -> None:
        self.context.config.preference_manager.selected_menu = value

    @override
    def do_process(self) -> None:
        widget = self._menus.get(self.selected_menu)
        if widget is not None:
            widget.do_preprocess()
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process(widget)
        finally:
            imgui.pop_style_var()
            if widget is not None:
                widget.do_postprocess()

    def do_child_process(
        self,
        widget: Optional[BasePreference] = None,
        *,
        child_flags=RESIZE_X | BORDERS,
    ) -> None:
        with begin_child_context("Menu", SIDE_MENU_WIDTH, child_flags=child_flags):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected_menu)[1]:
                            self.selected_menu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if widget is not None:
                imgui.text(self.selected_menu)
                imgui.separator()
                widget.do_process()
            else:
                text_centered("Please select a item")

# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Optional, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.preference._base import BasePreference, PreferenceInterface
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


@lru_cache
def create_preference_widget_types() -> Sequence[Type[BasePreference]]:
    from cvp.apps.player.modes.preference.appearance import AppearancePreference
    from cvp.apps.player.modes.preference.concurrency import ConcurrencyPreference
    from cvp.apps.player.modes.preference.developer import DeveloperPreference
    from cvp.apps.player.modes.preference.dtype import DtypePreference
    from cvp.apps.player.modes.preference.ffmpeg import FFmpegPreference
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

    return (
        AppearancePreference,
        ConcurrencyPreference,
        DeveloperPreference,
        DtypePreference,
        FFmpegPreference,
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
    )


def create_preference_widgets(context: Context):
    widget_types = create_preference_widget_types()
    return OrderedDict({wt.get_menu_name(): wt(context) for wt in widget_types})


class PreferenceMode(BaseMode):
    __cvp_mode_name__ = "Preference"

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
        widget = self._menus.get(self.selected)
        if widget is not None:
            widget.do_preprocess()
        try:
            with self.begin_mode_context():
                self.do_child_process(widget)
        finally:
            if widget is not None:
                widget.do_postprocess()

    def do_child_process(
        self,
        widget: Optional[BasePreference] = None,
        *,
        menu_split_x=150,
        menu_child_flags=RESIZE_X | BORDERS,
    ) -> None:
        with begin_child_context(
            "Menu",
            size=(menu_split_x, 0),
            child_flags=menu_child_flags,
        ):
            if imgui.begin_list_box("###MenuList", FIT_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if widget is not None:
                imgui.text(self.selected)
                imgui.separator()
                widget.do_process()
            else:
                text_centered("Please select a item")

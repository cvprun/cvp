# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Mapping

from imgui_bundle import imgui

from cvp.config.sections.preference import PreferenceManagerConfig
from cvp.renderer.context import RendererContext
from cvp.renderer.popup.propagator import PopupPropagator
from cvp.types.override import override
from cvp.widgets.manager import Manager
from cvp.windows.preference._base import PreferenceWidget
from cvp.windows.preference.ffmpeg import FFmpegPreference
from cvp.windows.preference.flow import FlowPreference


class PreferenceManager(Manager[PreferenceManagerConfig, PreferenceWidget]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.preference_manager,
            title="Preference",
            closable=True,
            flags=None,
        )

        menus = [
            FlowPreference(context),
            FFmpegPreference(context),
        ]

        self._menus = OrderedDict[str, PreferenceWidget]()

        for menu in menus:
            assert isinstance(menu, PreferenceWidget)
            self._menus[menu.label] = menu

            if not isinstance(menu, PopupPropagator):
                continue

            for popup in menu.popups:
                self.register_popup(popup)

    @override
    def query_menu_title(self, key: str, item: PreferenceWidget) -> str:
        return key

    @override
    def get_menus(self) -> Mapping[str, PreferenceWidget]:
        return self._menus

    @override
    def on_menu(self, key: str, item: PreferenceWidget) -> None:
        imgui.text(key)
        imgui.separator()
        item.on_process()

# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Callable

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.push_style_var import style_window_padding_context
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.types.override import override


class PreferenceMode(BaseMode):
    _menus: OrderedDict[str, Callable[[], None]]

    def __init__(self, context: RendererContext):
        super().__init__(context)

        self._menus = OrderedDict()
        self._menus["Appearance"] = self.on_appearance

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.preference

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @property
    def selected(self) -> str:
        return self.context.config.preference_manager.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.context.config.preference_manager.selected = value

    @override
    def do_process(self) -> None:
        set_next_window_as_viewport()
        with style_window_padding_context(0, 0):
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()

    def do_child_process(self, menu_label="Manu", main_label="Main", split_x=150.0):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", (-1, -1)):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            if main_callback := self._menus.get(self.selected):
                main_callback()
            else:
                text_centered("Please select a item")

    def on_appearance(self) -> None:
        text_centered("Appearance")

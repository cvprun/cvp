# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.window import ROOT_DOCKSPACE_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.msgs.msg import Msg
from cvp.types.override import override


class PreferenceMode(BaseMode):
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

    @override
    def do_process(self) -> None:
        set_next_window_as_viewport()
        with begin_context(type(self).__name__, flags=ROOT_DOCKSPACE_FLAGS):
            self.do_child_process()

    def do_child_process(self, menu_label="Manu", main_label="Main", split_x=150.0):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            imgui.text("Content")

        imgui.same_line()

        with begin_child_context(main_label):
            imgui.text("Content")

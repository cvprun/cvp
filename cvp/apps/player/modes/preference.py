# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.imgui.dockspace import dockspace_context
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
        with dockspace_context("RootDockspace"):
            imgui.begin("Left")
            imgui.text("Content")
            imgui.end()

            imgui.begin("Right")
            imgui.text("Content")
            imgui.end()

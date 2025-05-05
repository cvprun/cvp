# -*- coding: utf-8 -*-

from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.flows.flow._layout import FlowLayout
from cvp.context.context import Context
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_number__ = 3
    __cvp_mode_name__ = "Flow"

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = FlowLayout(context)

    @override
    def on_main_menu(self) -> None:
        if window := self._layout.focused_window:
            window.do_main_menu()

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        if window := self._layout.focused_window:
            window.do_keyboard_events()

    @override
    def do_process(self) -> None:
        self._layout.do_process()

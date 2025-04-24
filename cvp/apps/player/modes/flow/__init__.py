# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.flow._layout import _FlowLayout
from cvp.context.context import Context
from cvp.imgui.dockspace import dockspace_over_viewport_context
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.msgs.msg import Msg
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_number__ = 3
    __cvp_mode_name__ = "Flow"

    def __init__(self, context: Context):
        super().__init__(context)
        self._layout = _FlowLayout()
        self._windows = self._layout.create_windows(context)
        self._viewport_flags = ROOT_STATIC_VIEWPORT_FLAGS
        self._initialized_dock_layout = False

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
        viewport = imgui.get_main_viewport()
        with dockspace_over_viewport_context(viewport=viewport) as dockspace_id:
            assert isinstance(dockspace_id, int)
            assert 0 <= dockspace_id
            if not self._layout.initialized:
                self._layout.initialize_dock_layout(dockspace_id, viewport)

        for window in self._windows.values():
            window.do_process()

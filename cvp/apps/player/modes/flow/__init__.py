# -*- coding: utf-8 -*-

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.imgui.begin import begin_context
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.types.override import override


class FlowMode(BaseMode):
    __cvp_mode_name__ = "Flow"

    def __init__(self, context: RendererContext):
        super().__init__(context)

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
        # from cvp.imgui.dockspace import dockspace_over_viewport_context
        # with dockspace_over_viewport_context() as dockspace_id:
        #     assert isinstance(dockspace_id, int)
        #     assert 0 <= dockspace_id
        #     self.do_main_window()
        pass

    def do_main_window(self) -> None:
        with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
            pass

# -*- coding: utf-8 -*-

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.types.override import override


class IntroFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Intro"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            pass

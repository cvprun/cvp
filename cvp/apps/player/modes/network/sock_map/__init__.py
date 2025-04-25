# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class SockMapMode(BaseMode):
    __cvp_mode_name__ = "Socket Mapping"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                pass

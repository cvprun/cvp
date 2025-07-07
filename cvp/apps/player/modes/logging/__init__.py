# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import TEXT_LONG
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class LoggingMode(BaseMode):
    __cvp_mode_name__ = "Logging"
    __cvp_mode_icon__ = TEXT_LONG
    __cvp_mode_show__ = False

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                pass

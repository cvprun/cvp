# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import EMOTICON_DEVIL
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class MinidunMode(BaseMode):
    __cvp_mode_name__ = "Minidun"
    __cvp_mode_icon__ = EMOTICON_DEVIL

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                pass

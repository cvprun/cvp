# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FORMAT_LETTER_CASE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class CaseMode(BaseMode):
    __cvp_mode_name__ = "Case Converter"
    __cvp_mode_icon__ = FORMAT_LETTER_CASE

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.terminal

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                pass

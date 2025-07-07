# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FOCUS_FIELD
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class CalibrationMode(BaseMode):
    __cvp_mode_name__ = "Camera Calibration"
    __cvp_mode_icon__ = FOCUS_FIELD
    __cvp_mode_show__ = False

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

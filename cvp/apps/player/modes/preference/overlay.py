# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.config.sections.overlay import Anchor
from cvp.context.context import Context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.input_float import input_float
from cvp.imgui.slider_float import slider_float
from cvp.logging.logging import logger
from cvp.types.override import override


class OverlayPreference(BasePreference):
    __cvp_menu_name__ = "Overlay"

    def __init__(self, context: Context):
        super().__init__(context)
        self._anchors = list(Anchor)
        self._anchor_names = list(str(a.name) for a in Anchor)
        self._anchor_index = self._anchors.index(self.context.config.overlay.anchor)

    @property
    def config(self):
        return self.context.config.overlay

    @override
    def on_process(self) -> None:
        if opened_result := checkbox("Opened", self.config.opened):
            self.config.opened = opened_result.state

        if anchor_result := combo("Anchor", self._anchor_index, self._anchor_names):
            self._anchor_index = anchor_result.value
            self.config.anchor = self._anchors[anchor_result.value]
            logger.info(f"Changed anchor: {self.config.anchor}")

        if padding_result := input_float("Padding", self.config.padding):
            self.config.padding = padding_result.value
            logger.info(f"Changed padding: {padding_result.value}")

        if alpha_result := slider_float("Alpha", self.config.alpha, 0.0, 1.0):
            self.config.alpha = alpha_result.value
            logger.info(f"Changed alpha: {alpha_result.value}")

        warning_threshold = input_float(
            "FPS Warning Threshold",
            self.config.fps_warning_threshold,
        )
        if warning_threshold:
            self.config.fps_warning_threshold = warning_threshold.value
            logger.info(f"Changed fps_warning_threshold: {warning_threshold.value}")

        error_threshold = input_float(
            "FPS Error Threshold",
            self.config.fps_error_threshold,
        )
        if error_threshold:
            self.config.fps_error_threshold = error_threshold.value
            logger.info(f"Changed fps_error_threshold: {error_threshold.value}")

        if normal_color := color_edit4("Normal Color", *self.config.normal_color):
            self.config.normal_color = normal_color.color
            logger.info(f"Changed normal_color: {normal_color.color}")

        if warning_color := color_edit4("WarningColor", *self.config.warning_color):
            self.config.warning_color = warning_color.color
            logger.info(f"Changed warning_color: {warning_color.color}")

        if error_color := color_edit4("Error Color", *self.config.error_color):
            self.config.error_color = error_color.color
            logger.info(f"Changed error_color: {error_color.color}")

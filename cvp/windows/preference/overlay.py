# -*- coding: utf-8 -*-

from typing import List

from cvp.config.sections.overlay import Anchor
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.input_int import input_int
from cvp.imgui.slider_float import slider_float
from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class OverlayPreference(PreferenceWidget):
    _anchors: List[Anchor]

    def __init__(self, context: RendererContext, label="Overlay"):
        self._config = context.config.overlay_window
        self._label = label
        self._anchors = list(Anchor)
        self._anchor_names = [str(a.name) for a in Anchor]
        self._anchor_index = self._anchors.index(self._config.anchor)

    @property
    @override
    def label(self) -> str:
        return self._label

    @override
    def on_process(self) -> None:
        if anchor_result := combo("Anchor", self._anchor_index, self._anchor_names):
            self._anchor_index = anchor_result.value
            self._config.anchor = self._anchors[anchor_result.value]
            logger.info(f"Changed anchor: {self._config.anchor}")

        if padding_result := input_int("Padding", self._config.padding):
            self._config.padding = padding_result.value
            logger.info(f"Changed padding: {padding_result.value}")

        if alpha_result := slider_float("Alpha", self._config.alpha, 0.0, 1.0):
            self._config.alpha = alpha_result.value
            logger.info(f"Changed alpha: {alpha_result.value}")

        warning_threshold = input_int(
            "FPS Warning Threshold",
            self._config.fps_warning_threshold,
        )
        if warning_threshold:
            self._config.fps_warning_threshold = warning_threshold.value
            logger.info(f"Changed fps_warning_threshold: {warning_threshold.value}")

        error_threshold = input_int(
            "FPS Error Threshold",
            self._config.fps_error_threshold,
        )
        if error_threshold:
            self._config.fps_error_threshold = error_threshold.value
            logger.info(f"Changed fps_error_threshold: {error_threshold.value}")

        if normal_color := color_edit4("Normal Color", *self._config.normal_color):
            self._config.normal_color = normal_color.color
            logger.info(f"Changed normal_color: {normal_color.color}")

        if warning_color := color_edit4("WarningColor", *self._config.warning_color):
            self._config.warning_color = warning_color.color
            logger.info(f"Changed warning_color: {warning_color.color}")

        if error_color := color_edit4("Error Color", *self._config.error_color):
            self._config.error_color = error_color.color
            logger.info(f"Changed error_color: {error_color.color}")

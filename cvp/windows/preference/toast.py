# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.config.sections.toast import ToastWindowConfig
from cvp.imgui.color_edit3 import color_edit3
from cvp.imgui.drag_float import drag_float
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.slider_float2 import slider_float2
from cvp.inspect.member import get_public_instance_attributes
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class ToastPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Toast"):
        self._config = context.config.toast_window
        self._label = label
        self._mq = context.mq

    @property
    @override
    def label(self) -> str:
        return self._label

    @override
    def on_process(self) -> None:
        pivot_result = slider_float2(
            "Pivot",
            self._config.pivot_x,
            self._config.pivot_y,
            min_value=0.0,
            max_value=1.0,
        )
        if pivot_result:
            self._config.pivot = pivot_result.value

        anchor_result = slider_float2(
            "Anchor",
            self._config.anchor_x,
            self._config.anchor_y,
            min_value=0.0,
            max_value=1.0,
        )
        if anchor_result:
            self._config.anchor = anchor_result.value

        margin_result = drag_float2("Margin", *self._config.margin)
        if margin_result:
            self._config.margin = margin_result.values

        padding_result = drag_float2("Padding", *self._config.padding)
        if padding_result:
            self._config.padding = padding_result.values

        rounding_result = drag_float("Rounding", self._config.rounding)
        if rounding_result:
            self._config.rounding = rounding_result.value

        fadein_result = drag_float("Fadein", self._config.fadein)
        if fadein_result:
            self._config.fadein = fadein_result.value

        fadeout_result = drag_float("Fadeout", self._config.fadeout)
        if fadeout_result:
            self._config.fadeout = fadeout_result.value

        waiting_result = drag_float("Waiting", self._config.waiting)
        if waiting_result:
            self._config.waiting = waiting_result.value

        background_result = color_edit3("Background", *self._config.background_color)
        if background_result:
            self._config.background_color = background_result.color

        success_result = color_edit3("Success", *self._config.success_color)
        if success_result:
            self._config.success_color = success_result.color

        normal_result = color_edit3("Normal", *self._config.normal_color)
        if normal_result:
            self._config.normal_color = normal_result.color

        warning_result = color_edit3("Warning", *self._config.warning_color)
        if warning_result:
            self._config.warning_color = warning_result.color

        error_result = color_edit3("Error", *self._config.error_color)
        if error_result:
            self._config.error_color = error_result.color

        if imgui.button("Set defaults"):
            default_config = ToastWindowConfig()
            for key, value in get_public_instance_attributes(default_config):
                setattr(self._config, key, value)

        imgui.separator()

        if imgui.button("Show Demo Toast"):
            self._mq.append_toast("Demo Toast")

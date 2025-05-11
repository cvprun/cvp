# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.config.sections.toast import ToastConfig
from cvp.context.context import Context
from cvp.imgui.color_edit3 import color_edit3
from cvp.imgui.drag_float import drag_float
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.slider_float2 import slider_float2
from cvp.inspect.member import get_public_instance_attributes
from cvp.types.override import override


class ToastPreference(BasePreference):
    __cvp_menu_name__ = "Toast"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.toast

    @override
    def on_process(self) -> None:
        pivot_result = slider_float2(
            "Pivot",
            self.config.pivot_x,
            self.config.pivot_y,
            min_value=0.0,
            max_value=1.0,
        )
        if pivot_result:
            self.config.pivot = pivot_result.value

        anchor_result = slider_float2(
            "Anchor",
            self.config.anchor_x,
            self.config.anchor_y,
            min_value=0.0,
            max_value=1.0,
        )
        if anchor_result:
            self.config.anchor = anchor_result.value

        margin_result = drag_float2("Margin", *self.config.margin)
        if margin_result:
            self.config.margin = margin_result.values

        padding_result = drag_float2("Padding", *self.config.padding)
        if padding_result:
            self.config.padding = padding_result.values

        rounding_result = drag_float("Rounding", self.config.rounding)
        if rounding_result:
            self.config.rounding = rounding_result.value

        fadein_result = drag_float("Fadein", self.config.fadein)
        if fadein_result:
            self.config.fadein = fadein_result.value

        fadeout_result = drag_float("Fadeout", self.config.fadeout)
        if fadeout_result:
            self.config.fadeout = fadeout_result.value

        waiting_result = drag_float("Waiting", self.config.waiting)
        if waiting_result:
            self.config.waiting = waiting_result.value

        background_result = color_edit3("Background", *self.config.background_color)
        if background_result:
            self.config.background_color = background_result.color

        success_result = color_edit3("Success", *self.config.success_color)
        if success_result:
            self.config.success_color = success_result.color

        normal_result = color_edit3("Normal", *self.config.normal_color)
        if normal_result:
            self.config.normal_color = normal_result.color

        warning_result = color_edit3("Warning", *self.config.warning_color)
        if warning_result:
            self.config.warning_color = warning_result.color

        error_result = color_edit3("Error", *self.config.error_color)
        if error_result:
            self.config.error_color = error_result.color

        if imgui.button("Reset defaults"):
            default_config = ToastConfig()
            for key, value in get_public_instance_attributes(default_config):
                setattr(self.config, key, value)

        if imgui.button("Show Demo Toast"):
            self.context.msgs.append_toast("Demo Toast")

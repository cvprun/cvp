# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo_encoding import combo_text_encoding
from cvp.imgui.combo_enum import combo_enum
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.types.override import override


class TailPreference(BasePreference):
    __cvp_menu_name__ = "Tail"

    def __init__(self, context: Context):
        super().__init__(context)
        self.encoding_filter = str()
        self.error_filter = str()

    @property
    def config(self):
        return self.context.config.tail

    @override
    def on_process(self) -> None:
        if default_encoding := combo_text_encoding(
            label="Default Encoding",
            value=self.config.normalize_encoding,
            filter_value=self.encoding_filter,
        ):
            self.config.encoding = default_encoding.encoding
            self.encoding_filter = default_encoding.filter_value

        if error_handling := combo_enum(
            label="Default Error Handling",
            value=self.config.codec_error_handling,
        ):
            assert isinstance(error_handling.item, str)
            self.config.errors = error_handling.item

        if tabs_always := checkbox("Show tabs always", self.config.show_tabs_always):
            self.config.show_tabs_always = tabs_always.state

        if autoscroll := checkbox("Autoscroll", self.config.autoscroll):
            self.config.autoscroll = autoscroll.state

        if lines := input_int("Max buffer lines", self.config.max_buffer_lines):
            self.config.max_buffer_lines = lines.value
        if button("Infinite"):
            self.config.update_infinite_lines()

        if manually_update_interval := input_float(
            "Manually update interval (seconds)",
            self.config.manually_update_interval,
        ):
            self.config.manually_update_interval = manually_update_interval.value

        if button("Default"):
            self.config.update_defaults()

# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.combo_encoding import combo_text_encoding
from cvp.types.override import override


class TextPreference(BasePreference):
    __cvp_menu_name__ = "Text Editor"

    def __init__(self, context: Context):
        super().__init__(context)
        self.encoding_filter = str()
        self.timezone_filter = str()

    @property
    def config(self):
        return self.context.config.text

    @override
    def on_process(self) -> None:
        if default_encoding := combo_text_encoding(
            label="Default Encoding",
            value=self.config.default_encoding,
            filter_value=self.encoding_filter,
        ):
            self.config.default_encoding = default_encoding.tzname
            self.encoding_filter = default_encoding.filter_value

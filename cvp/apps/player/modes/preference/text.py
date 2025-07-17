# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.combo_timezone import combo_timezone
from cvp.types.override import override


class TextPreference(BasePreference):
    __cvp_menu_name__ = "Text Editor"

    def __init__(self, context: Context):
        super().__init__(context)
        self.timezone_filter = str()

    @property
    def config(self):
        return self.context.config.text

    @property
    def default_timezone(self) -> str:
        return self.config.default_timezone

    @default_timezone.setter
    def default_timezone(self, value: str) -> None:
        self.config.default_timezone = value

    @override
    def on_process(self) -> None:
        if result := combo_timezone(
            "TimeZone",
            self.default_timezone,
            filter_value=self.timezone_filter,
        ):
            self.default_timezone = result.tzname
            self.timezone_filter = result.filter_value

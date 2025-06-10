# -*- coding: utf-8 -*-

from typing import Final
from zoneinfo import ZoneInfo, available_timezones

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import WEB_CLOCK
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.imgui.flags.table_column import WIDTH_STRETCH
from cvp.imgui.input_text_with_hint import input_text_with_hint
from cvp.types.override import override


class TimeZoneMode(BaseMode):
    __cvp_mode_name__ = "TimeZone"
    __cvp_mode_icon__ = WEB_CLOCK

    _TABLE_COLUMNS: Final[int] = 3
    _TABLE_FLAGS: Final[int] = DEFAULT_TABLE_FLAGS

    def __init__(self, context: Context):
        super().__init__(context)
        self._timezones = [ZoneInfo(tz) for tz in sorted(available_timezones())]
        self._filter = str()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                imgui.text("Available TimeZones")
                imgui.separator()
                self.do_child_process()

    def do_child_process(self) -> None:
        imgui.set_next_item_width(FIT_WIDTH)
        self._filter = input_text_with_hint(
            label="##Filter",
            hint="Type to filter the list",
            value=self._filter,
        ).value

        if imgui.begin_table("Table", self._TABLE_COLUMNS, self._TABLE_FLAGS):
            try:
                imgui.table_setup_column("Region", WIDTH_STRETCH)
                imgui.table_setup_column("City", WIDTH_STRETCH)
                imgui.table_setup_column("Offset", WIDTH_STRETCH)
                imgui.table_headers_row()

                for timezone in self._timezones:
                    if self._filter:
                        normalized_key = timezone.key.lower().strip()
                        normalized_filter = self._filter.lower().strip()
                        if normalized_key.find(normalized_filter) == -1:
                            continue

                    imgui.table_next_row()
                    tz_keys = timezone.key.split("/", maxsplit=1)
                    region = tz_keys[0]
                    city = tz_keys[1] if 2 <= len(tz_keys) else str()

                    imgui.table_set_column_index(0)
                    imgui.text(region)

                    imgui.table_set_column_index(1)
                    imgui.text(city)

                    utc_offset = str(timezone.utcoffset(None))
                    imgui.table_set_column_index(2)
                    imgui.text(utc_offset)
            finally:
                imgui.end_table()

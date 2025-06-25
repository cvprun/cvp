# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags import table_column
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_value import input_text_value
from cvp.mediamtx.item import MediamtxItem
from cvp.variables import NOT_FOUND_INDEX


class MediamtxConfigTab:
    def __init__(self, context: Context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def __call__(self, mediamtx: MediamtxItem) -> None:
        imgui.text(mediamtx.name)
        imgui.separator()

        if mediamtx.has_error:
            self.text_error(str(mediamtx.error))

        mediamtx.name = input_text_value("MediaMTX Name", mediamtx.name)
        mediamtx.url = input_text_value("MediaMTX URL", mediamtx.url)

        imgui.text("Headers")
        imgui.same_line()
        if imgui.small_button("Add"):
            mediamtx.headers.append((str(), str()))

        if imgui.begin_table("Headers", 3, DEFAULT_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Key", table_column.WIDTH_STRETCH)
                imgui.table_setup_column("Value", table_column.WIDTH_STRETCH)
                imgui.table_setup_column("Action", table_column.WIDTH_FIXED)
                imgui.table_headers_row()

                remove_index = NOT_FOUND_INDEX

                for i in range(len(mediamtx.headers)):
                    key, value = mediamtx.headers[i]

                    imgui.table_next_row()

                    imgui.table_set_column_index(0)
                    imgui.set_next_item_width(FIT_WIDTH)
                    key_result = imgui.input_text(f"###HeaderKey{i}", key)
                    if key_result[0]:
                        mediamtx.headers[i] = key_result[1], value

                    imgui.table_set_column_index(1)
                    imgui.set_next_item_width(FIT_WIDTH)
                    val_result = imgui.input_text(f"###HeaderValue{i}", value)
                    if val_result[0]:
                        mediamtx.headers[i] = key, val_result[1]

                    imgui.table_set_column_index(2)
                    if imgui.button(f"Del###Del{i}"):
                        remove_index = i

                if remove_index != NOT_FOUND_INDEX:
                    mediamtx.headers.pop(remove_index)

                imgui.get_column_width(0)
            finally:
                imgui.end_table()

        if redirect := checkbox("Follow redirects", mediamtx.follow_redirects):
            mediamtx.follow_redirects = redirect.state

        if timeout := input_float("HTTP timeout (seconds)", mediamtx.timeout, 1.0):
            mediamtx.timeout = timeout.value

# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.widgets.table_simple_kvs import table_simple_kvs
from cvp.mediamtx.item import MediamtxItem


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

        mediamtx.name = input_text_value("MediaMTX Name", mediamtx.name)
        mediamtx.url = input_text_value("MediaMTX URL", mediamtx.url)

        imgui.text("Headers")
        table_simple_kvs(
            "Headers",
            mediamtx.headers,
            swappable=True,
            removable=True,
            insertable=True,
        )

        if redirect := checkbox("Follow redirects", mediamtx.follow_redirects):
            mediamtx.follow_redirects = redirect.state

        if timeout := input_float("HTTP timeout (seconds)", mediamtx.timeout, 1.0):
            mediamtx.timeout = timeout.value

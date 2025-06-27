# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox_value import checkbox_value
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import RESIZE_X
from cvp.imgui.input_int_value import input_int_value
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.begin_table_mutable_sequence import begin_table_mutable_sequence
from cvp.mediamtx.client import Path
from cvp.mediamtx.item import MediamtxItem


class MediamtxPathTab:
    _API_SPLIT_X: Final[int] = 150
    _API_CHILD_FLAGS: Final[int] = RESIZE_X

    def __init__(self, context: Context):
        self._context = context
        self._runner = context.create_thread_runner(self.on_update_paths_main)

    @property
    def context(self):
        return self._context

    @staticmethod
    def on_update_paths_main(mediamtx: MediamtxItem):
        mediamtx.update_paths()

    def get_selected_path(self, mediamtx: MediamtxItem) -> str:
        return self.context.get_selected_submenu(type(self), suffix=mediamtx.uuid)

    def set_selected_path(self, mediamtx: MediamtxItem, value: str) -> None:
        self.context.set_selected_submenu(type(self), value, suffix=mediamtx.uuid)

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def __call__(self, mediamtx: MediamtxItem) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        with begin_child_context(
            label="APIList",
            size=(self._API_SPLIT_X, 0),
            child_flags=self._API_CHILD_FLAGS,
        ):
            if button("Reload", disabled=running):
                self._runner(mediamtx)

            if imgui.begin_list_box("##APIList", size=FIT_SIZE):
                try:
                    if mediamtx.paths:
                        for path in mediamtx.paths.items or []:
                            selected = path.name == self.get_selected_path(mediamtx)
                            if imgui.selectable(path.name, selected)[1]:
                                self.set_selected_path(mediamtx, path.name)
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("APIMain", size=FIT_SIZE):
            if running:
                text_centered("Requesting a list of path...")
            elif has_error:
                assert not running
                self.text_error(str(self._runner.error))
            else:
                assert not running
                assert not has_error
                path_name = self.get_selected_path(mediamtx)
                media_path = mediamtx.get_path(path_name)
                if media_path is None:
                    text_centered("Please select a item")
                    return

                with style_disable_input_context():
                    self.do_mediamtx_path(media_path)

    @staticmethod
    def do_mediamtx_path(path: Path) -> None:
        input_text_value("name", path.name)

        input_text_value("confName", path.confName)
        input_text_value("source", str(path.source))
        checkbox_value("ready", path.ready)
        input_text_value("readyTime", path.readyTime)
        begin_table_mutable_sequence("tracks", path.tracks)
        input_int_value("bytesReceived", path.bytesReceived)
        input_int_value("bytesSent", path.bytesSent)

        imgui.text("Readers")
        for reader in path.readers:
            imgui.bullet()
            imgui.same_line()
            imgui.text(reader.type)
            imgui.same_line()
            imgui.text(reader.id)

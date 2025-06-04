# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.service.item import ServiceItem
from cvp.variables import (
    STDERR_FILE_HANDLE,
    STDERR_FILE_NAME,
    STDOUT_FILE_HANDLE,
    STDOUT_FILE_NAME,
)


class ServicesLoggingTab:

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context, handle: int):
        self._context = context
        self._handle = handle
        self._selected_file = str()

        if handle not in (STDOUT_FILE_HANDLE, STDERR_FILE_HANDLE):
            raise ValueError(f"Unsupported handle number: {handle}")

        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove file?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all files?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

        self._popups = PopupList(
            self._confirm_remove,
            self._confirm_clear,
        )

    @property
    def context(self):
        return self._context

    @property
    def popups(self):
        return self._popups

    @property
    def handle(self):
        return self._handle

    @property
    def handle_name(self):
        if self._handle == STDOUT_FILE_HANDLE:
            return STDERR_FILE_NAME
        else:
            assert self._handle == STDERR_FILE_HANDLE
            return STDOUT_FILE_NAME

    # @property
    # def services(self):
    #     return self.context.services

    @property
    def files(self):
        return list()

    def get_stream(self, service: ServiceItem):
        if self._handle == STDOUT_FILE_HANDLE:
            assert service.stdout.type == STDOUT_FILE_HANDLE
            return service.stdout
        else:
            assert self._handle == STDERR_FILE_HANDLE
            assert service.stderr.type == STDERR_FILE_HANDLE
            return service.stderr

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        self._remove_candidate = str()

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return

    def __call__(self, service: ServiceItem) -> None:
        imgui.text(self.handle_name.capitalize() + " Logging")
        imgui.separator()

        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if button("Reload"):
                # self.services.read_all_config_files()
                pass
            imgui.same_line()
            if button("Del", disabled=self._selected_file not in self.files):
                self._remove_candidate = self._selected_file
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.files):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for file in self.files:
                        selected = file == self._selected_file
                        if imgui.selectable(file, selected)[1]:
                            self._selected_file = file
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if self._selected_file in self.files:
                self.do_file_process(self._selected_file)
            else:
                text_centered("Please select a item")

    def do_file_process(self, file: str) -> None:
        pass

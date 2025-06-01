# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.service.item import ServiceItem
from cvp.variables import (
    STDERR_FILE_HANDLE,
    STDERR_FILE_NAME,
    STDOUT_FILE_HANDLE,
    STDOUT_FILE_NAME,
)


class ServicesLoggingTab:
    def __init__(self, context: Context, handle: int):
        self._context = context
        self._handle = handle

        if handle not in (STDOUT_FILE_HANDLE, STDERR_FILE_HANDLE):
            raise ValueError(f"Unsupported handle number: {handle}")

    @property
    def context(self):
        return self._context

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

    @property
    def services(self):
        return self.context.services

    def get_stream(self, service: ServiceItem):
        if self._handle == STDOUT_FILE_HANDLE:
            assert service.stdout.type == STDOUT_FILE_HANDLE
            return service.stdout
        else:
            assert self._handle == STDERR_FILE_HANDLE
            assert service.stderr.type == STDERR_FILE_HANDLE
            return service.stderr

    def __call__(self, service: ServiceItem) -> None:
        imgui.text(self.handle_name.capitalize() + " Logging")

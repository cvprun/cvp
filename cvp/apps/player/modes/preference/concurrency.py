# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.text_colored import text_colored
from cvp.logging.logging import logger
from cvp.types.override import override


class ConcurrencyPreference(BasePreference):
    __cvp_menu_name__ = "Concurrency"

    def __init__(self, context: Context):
        super().__init__(context)
        self._show_restart = False

    @property
    def config(self):
        return self.context.config.concurrency

    @property
    def thread_name_prefix(self) -> str:
        return self.config.thread_name_prefix

    @thread_name_prefix.setter
    def thread_name_prefix(self, value: str):
        self.config.thread_name_prefix = value

    @property
    def thread_workers(self) -> int:
        return self.config.thread_workers

    @thread_workers.setter
    def thread_workers(self, value: int):
        self.config.thread_workers = value

    @property
    def process_workers(self) -> int:
        return self.config.process_workers

    @process_workers.setter
    def process_workers(self, value: int):
        self.config.process_workers = value

    @override
    def do_process(self) -> None:
        if prefix_result := input_text("Thread Name Prefix", self.thread_name_prefix):
            self.thread_name_prefix = prefix_result.value
            self._show_restart = True
            logger.info(f"Changed thread name prefix: '{prefix_result.value}'")

        if thread_workers_result := input_int("Thread Workers", self.thread_workers):
            self.thread_workers = thread_workers_result.value
            self._show_restart = True
            logger.info(f"Changed thread workers level: {thread_workers_result.value}")

        if process_workers_result := input_int("Process Workers", self.process_workers):
            self.process_workers = process_workers_result.value
            self._show_restart = True
            logger.info(f"Changed process workers: {process_workers_result.value}")

        if self._show_restart:
            imgui.separator()
            text_colored("The change is applied after the start", (1.0, 0.1, 0.1, 1.0))

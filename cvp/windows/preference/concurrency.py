# -*- coding: utf-8 -*-

import imgui

from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class ConcurrencyPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Concurrency"):
        self._config = context.config.concurrency
        self._label = label
        self._show_restart = False

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    def thread_workers(self) -> int:
        return self._config.thread_workers

    @thread_workers.setter
    def thread_workers(self, value: int):
        self._config.thread_workers = value

    @property
    def process_workers(self) -> int:
        return self._config.process_workers

    @process_workers.setter
    def process_workers(self, value: int):
        self._config.process_workers = value

    @override
    def on_process(self) -> None:
        imgui.text("Thread workers:")
        thread_workers_result = imgui.input_int(
            "##ThreadWorkers",
            self.thread_workers,
        )

        thread_workers_changed = thread_workers_result[0]
        thread_workers_value = thread_workers_result[1]
        assert isinstance(thread_workers_value, int)

        if thread_workers_changed:
            self.thread_workers = thread_workers_value
            self._show_restart = True
            logger.info(f"Changed thread workers level: {thread_workers_value}")

        imgui.text("Process workers:")
        process_workers_result = imgui.input_int(
            "##ProcessWorkers",
            self.process_workers,
        )

        process_workers_changed = process_workers_result[0]
        process_workers_value = process_workers_result[1]
        assert isinstance(process_workers_value, int)

        if process_workers_changed:
            self.process_workers = process_workers_value
            self._show_restart = True
            logger.info(f"Changed process workers: {process_workers_value}")

        if self._show_restart:
            imgui.separator()
            imgui.text_colored("The change is applied after the start", 1.0, 0.1, 0.1)

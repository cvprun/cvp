# -*- coding: utf-8 -*-

import os
import sys
from functools import lru_cache
from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.text_colored import text_colored
from cvp.imgui.tooltip import hovered_tooltip_text_wrapped
from cvp.logging.logging import logger
from cvp.types.override import override

# On Windows, WaitForMultipleObjects is used to wait for processes to finish.
# It can wait on, at most, 63 objects. There is an overhead of two objects:
# - the result queue reader
# - the thread wakeup reader
MAX_WINDOWS_PROCESS_WORKERS: Final[int] = 63 - 2

MIN_THREAD_WORKERS: Final[int] = 5
MIN_PROCESS_WORKERS: Final[int] = 1


@lru_cache
def cpu_count() -> int:
    count = os.cpu_count()
    return count if count is not None else 1


def valid_thread_workers(value: int) -> int:
    if value < MIN_THREAD_WORKERS:
        return MIN_THREAD_WORKERS

    max_thread_workers = min(32, cpu_count() + 4)
    if max_thread_workers < value:
        return max_thread_workers

    return value


def valid_process_workers(value: int) -> int:
    if value < MIN_PROCESS_WORKERS:
        return MIN_PROCESS_WORKERS

    is_win32 = sys.platform == "win32"
    if is_win32 and MAX_WINDOWS_PROCESS_WORKERS < value:
        return MAX_WINDOWS_PROCESS_WORKERS

    return value


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

        hovered_tooltip_text_wrapped(
            "Added the thread_name_prefix parameter to allow users to control the "
            "threading.Thread names for worker threads created by the pool for easier "
            "debugging."
        )

        if thread_workers_result := input_int("Thread Workers", self.thread_workers):
            self.thread_workers = valid_thread_workers(thread_workers_result.value)
            self._show_restart = True
            logger.info(f"Changed thread workers level: {thread_workers_result.value}")

        hovered_tooltip_text_wrapped(
            "The maximum number of threads that can be used to execute the given calls."
            "Default value of max_workers is changed to `min(32, os.cpu_count() + 4)`. "
            "This default value preserves at least 5 workers for I/O bound tasks. It "
            "utilizes at most 32 CPU cores for CPU bound tasks which release the GIL. "
            "And it avoids using very large resources implicitly on many-core machines."
        )

        if process_workers_result := input_int("Process Workers", self.process_workers):
            self.process_workers = valid_process_workers(process_workers_result.value)
            self._show_restart = True
            logger.info(f"Changed process workers: {process_workers_result.value}")

        hovered_tooltip_text_wrapped(
            "The maximum number of processes that can be used to execute the given "
            "calls. If None or not given then as many worker processes will be created "
            "as the machine has processors."
        )

        if self._show_restart:
            imgui.separator()
            text_colored("The change is applied after the start", (1.0, 0.1, 0.1, 1.0))

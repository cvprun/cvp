# -*- coding: utf-8 -*-

from time import time
from typing import Dict, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.assets.fonts.mdi import APPLICATION
from cvp.context.context import Context
from cvp.imgui.flags.table import DEFAULT_TABLE_FLAGS
from cvp.psutil.process.state import (
    PROCESS_STATE_TITLES,
    ProcessState,
    query_all_process_states,
)
from cvp.types.override import override


class ProcessesSystem(BaseSystem):
    __cvp_menu_name__ = "Processes"
    __cvp_menu_icon__ = APPLICATION

    _states: Dict[int, ProcessState]
    _error: Optional[BaseException]

    def __init__(self, context: Context):
        super().__init__(context)
        self._runner = context.create_thread_runner(self.on_query_all_process_states)
        self._states = dict()
        self._error = None
        self._interval = 1.0
        self._latest_time = 0.0

    @staticmethod
    def on_query_all_process_states():
        return query_all_process_states()

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    @override
    def on_process(self) -> None:
        if not self._runner.running:
            if self._runner.future is not None:
                self._states = self._runner.result or dict()
                self._error = self._runner.error
                self._runner.clear()

            assert self._runner.future is None
            assert self._runner.result is None
            assert self._runner.error is None

            current = time()
            if self._interval <= current - self._latest_time:
                self._latest_time = current
                self._runner()

        if self._error is not None:
            self.text_error(str(self._error))

        self.do_processes_table()

    def do_processes_table(self) -> None:
        if imgui.begin_table("Table", len(PROCESS_STATE_TITLES), DEFAULT_TABLE_FLAGS):
            try:
                for header in PROCESS_STATE_TITLES.values():
                    imgui.table_setup_column(header)
                imgui.table_headers_row()

                # sort_specs = imgui.table_get_sort_specs()
                # if sort_specs:
                #     _U = 0  # user_selected_column_index
                #     column_index = sort_specs.get_specs(_U).column_index
                #     sort_order = sort_specs.get_specs(_U).sort_order
                #     sort_direction = sort_specs.get_specs(_U).sort_direction
                #     if sort_direction == imgui.SortDirection.ascending:
                #         pass
                #     elif sort_direction == imgui.SortDirection.descending:
                #         pass
                #     else:
                #         assert sort_direction == imgui.SortDirection.none

                for proc in self._states.values():
                    imgui.table_next_row()
                    for i, key in enumerate(PROCESS_STATE_TITLES.keys()):
                        imgui.table_set_column_index(i)
                        imgui.text(str(getattr(proc, key)))
            finally:
                imgui.end_table()

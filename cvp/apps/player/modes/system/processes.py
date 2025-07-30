# -*- coding: utf-8 -*-

from time import time
from typing import Final, List, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.assets.fonts.mdi import APPLICATION
from cvp.context.context import Context
from cvp.imgui.flags import table
from cvp.imgui.table_sort_specs import SortDirection, TableSortSpec, sort_specs_by_order
from cvp.psutil.process.state import PROCESS_STATE_TITLES, query_all_process_states
from cvp.types.override import override


class ProcessesSystem(BaseSystem):
    __cvp_menu_name__ = "Processes"
    __cvp_menu_icon__ = APPLICATION

    _TABLE_FLAGS: Final[int] = table.merge_table_flags(
        table.RESIZABLE,
        table.REORDERABLE,
        table.HIDEABLE,
        table.SORTABLE,
        table.ROW_BG,
        table.BORDERS_OUTER,
        table.BORDERS_V,
        table.NO_BORDERS_IN_BODY,
        table.SCROLL_Y,
        table.BORDERS,
        table.SORT_TRISTATE,
    )

    _sort_specs: List[TableSortSpec]
    _error: Optional[BaseException]

    def __init__(self, context: Context):
        super().__init__(context)
        self._runner = context.create_thread_runner(self.on_query_all_process_states)
        self._states = query_all_process_states()
        self._sort_specs = list()
        self._error = None
        self._interval = 1.0
        self._latest_time = 0.0
        self._headers = list(PROCESS_STATE_TITLES.items())

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
        if imgui.begin_table("Table", len(self._headers), self._TABLE_FLAGS):
            try:
                for _, header_title in self._headers:
                    imgui.table_setup_column(header_title)

                imgui.table_setup_scroll_freeze(0, 1)
                imgui.table_headers_row()

                sort_specs = imgui.table_get_sort_specs()
                if sort_specs.specs_dirty:
                    self._sort_specs = sort_specs_by_order(sort_specs)
                    sort_specs.specs_dirty = False

                states = list(self._states.values())
                assert len(self._sort_specs) in (0, 1)
                if self._sort_specs:
                    sort_spec = self._sort_specs[0]
                    header_key, _ = self._headers[sort_spec.column]
                    ascending = sort_spec.direction == SortDirection.ascending
                    states.sort(key=lambda x: getattr(x, header_key), reverse=ascending)

                clipper = imgui.ListClipper()
                clipper.begin(len(states))
                while clipper.step():
                    for i in range(clipper.display_start, clipper.display_end):
                        proc = states[i]

                        imgui.table_next_row()
                        for header_index, header in enumerate(self._headers):
                            header_key, _ = header
                            imgui.table_set_column_index(header_index)
                            imgui.text(str(getattr(proc, header_key)))
            finally:
                imgui.end_table()

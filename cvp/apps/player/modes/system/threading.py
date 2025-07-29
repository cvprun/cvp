# -*- coding: utf-8 -*-

import threading
from typing import Any, Callable, Final, List, NamedTuple

from imgui_bundle import imgui

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.assets.fonts.mdi import MULTICAST
from cvp.context.context import Context
from cvp.imgui.flags import table, table_column
from cvp.imgui.table_sort_specs import SortDirection, TableSortSpec, sort_specs_by_order
from cvp.types.override import override
from cvp.variables import UNKNOWN_THREAD_IDENT


class ThreadingSystem(BaseSystem):
    __cvp_menu_name__ = "Threading"
    __cvp_menu_icon__ = MULTICAST

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

    def __init__(self, context: Context):
        super().__init__(context)
        self._headers = self._create_columns()
        self._sort_specs = list()

    @staticmethod
    def _key_thread_ident(thread: threading.Thread) -> int:
        return thread.ident if thread.ident is not None else UNKNOWN_THREAD_IDENT

    @staticmethod
    def _key_thread_name(thread: threading.Thread) -> str:
        return thread.name

    @staticmethod
    def _key_thread_alive(thread: threading.Thread) -> bool:
        return thread.is_alive()

    @staticmethod
    def _key_thread_daemon(thread: threading.Thread) -> bool:
        return thread.daemon

    class _ThreadColumn(NamedTuple):
        name: str
        key: Callable[[threading.Thread], Any]
        flags: int

    @classmethod
    def _create_columns(cls) -> List[_ThreadColumn]:
        _tc = table_column
        _ident_flags = _tc.WIDTH_FIXED | _tc.DEFAULT_SORT
        return [
            cls._ThreadColumn("Identifier", cls._key_thread_ident, _ident_flags),
            cls._ThreadColumn("Name", cls._key_thread_name, _tc.WIDTH_STRETCH),
            cls._ThreadColumn("Alive", cls._key_thread_alive, _tc.WIDTH_FIXED),
            cls._ThreadColumn("Daemon", cls._key_thread_daemon, _tc.WIDTH_FIXED),
        ]

    @override
    def on_process(self) -> None:
        imgui.text("Thread Monitoring")
        imgui.separator()

        if imgui.begin_table("Table", len(self._headers), self._TABLE_FLAGS):
            try:
                for i, header in enumerate(self._headers):
                    imgui.table_setup_column(
                        header.name,
                        header.flags,
                        0.0,
                        i,
                    )

                imgui.table_setup_scroll_freeze(0, 1)
                imgui.table_headers_row()

                sort_specs = imgui.table_get_sort_specs()
                if sort_specs.specs_dirty:
                    self._sort_specs = sort_specs_by_order(sort_specs)
                    sort_specs.specs_dirty = False

                threads = threading.enumerate().copy()
                assert len(self._sort_specs) in (0, 1)
                if self._sort_specs:
                    sort_spec = self._sort_specs[0]
                    sort_key = self._headers[sort_spec.column].key
                    sort_ascending = sort_spec.direction == SortDirection.ascending
                    threads.sort(key=sort_key, reverse=sort_ascending)

                clipper = imgui.ListClipper()
                clipper.begin(len(threads))
                while clipper.step():
                    for i in range(clipper.display_start, clipper.display_end):
                        thread = threads[i]

                        imgui.table_next_row()

                        imgui.table_next_column()
                        ident = str(thread.ident) if thread.ident is not None else "-"
                        imgui.text(ident)

                        imgui.table_next_column()
                        imgui.text(thread.name)

                        imgui.table_next_column()
                        imgui.text(str(thread.is_alive()))

                        imgui.table_next_column()
                        imgui.text(str(thread.daemon))
            finally:
                imgui.end_table()

# -*- coding: utf-8 -*-

from collections import deque
from copy import deepcopy
from typing import Deque, NamedTuple, Optional

from cvp.flow.graph import FlowGraph


class HistoryItem(NamedTuple):
    title: str
    graph: FlowGraph
    details: str


class FlowHistory:
    _records: Deque[HistoryItem]
    _eof: int

    def __init__(self, max_history: Optional[int] = None):
        self._records = deque(maxlen=max_history)
        self._eof = 0

    @property
    def records(self):
        return self._records

    @property
    def cursor_index(self):
        return self._eof - 1

    def __len__(self):
        return self._records.__len__()

    def __iter__(self):
        return self._records.__iter__()

    def __getitem__(self, index: int):
        return self._records.__getitem__(index)

    def __setitem__(self, index: int, value: HistoryItem) -> None:
        self._records.__setitem__(index, value)

    def __bool__(self):
        return bool(self._records)

    @property
    def undoable(self) -> bool:
        if len(self._records) < 2:
            return False
        next_index = self.cursor_index - 1
        return 0 <= next_index < len(self._records)

    @property
    def redoable(self):
        if len(self._records) < 2:
            return False
        next_index = self.cursor_index + 1
        return 0 <= next_index < len(self._records)

    @property
    def max_history(self):
        return self._records.maxlen

    def normalize_index(self, index: int) -> int:
        if index < 0:
            index += len(self._records)
        assert 0 <= index < len(self._records)
        return index

    def update_max_history(self, value: Optional[int] = None) -> None:
        if self._records.maxlen == value:
            return
        cls = self._records.__class__
        self._records = cls(self._records, maxlen=value)

    def clear_history(self) -> None:
        self._records.clear()
        self._eof = 0

    def save_history(
        self,
        title: str,
        graph: FlowGraph,
        details: Optional[str] = None,
        *,
        max_history: Optional[int] = None,
        freeze_latest=False,
    ) -> HistoryItem:
        if max_history is not None:
            self.update_max_history(max_history)

        while self._eof < len(self._records):
            self._records.pop()

        if details is None:
            details = str()

        item = HistoryItem(title, deepcopy(graph), details)
        self._records.append(item)
        if not freeze_latest:
            self._eof = len(self._records)
        return item

    def load_history(self, index: int, *, freeze_latest=False) -> FlowGraph:
        index = self.normalize_index(index)
        item = self._records[index]
        if not freeze_latest:
            self._eof = index + 1
        return deepcopy(item.graph)

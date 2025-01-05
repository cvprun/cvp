# -*- coding: utf-8 -*-

from collections import deque
from copy import deepcopy
from typing import Deque, NamedTuple, Optional

from cvp.flow.datas.graph import Graph


class RecordItem(NamedTuple):
    title: str
    graph: Graph
    details: str


class History:
    _items: Deque[RecordItem]
    _latest: int

    def __init__(self, max_history: Optional[int] = None):
        self._items = deque(maxlen=max_history)
        self._latest = 0

    @property
    def items(self):
        return self._items

    @property
    def latest(self):
        return self._latest

    def __len__(self):
        return self._items.__len__()

    def __iter__(self):
        return self._items.__iter__()

    def __getitem__(self, index: int):
        return self._items.__getitem__(index)

    def __setitem__(self, index: int, value: RecordItem) -> None:
        self._items.__setitem__(index, value)

    @property
    def max_history(self):
        return self._items.maxlen

    def update_max_history(self, value: Optional[int] = None) -> None:
        if self._items.maxlen == value:
            return
        cls = self._items.__class__
        self._items = cls(self._items, maxlen=value)

    def clear_history(self) -> None:
        self._items.clear()
        self._latest = 0

    def save_history(
        self,
        title: str,
        graph: Graph,
        details: Optional[str] = None,
        *,
        max_history: Optional[int] = None,
        freeze_latest=False,
    ) -> RecordItem:
        if max_history is not None:
            self.update_max_history(max_history)

        assert 0 <= self._latest
        while self._latest < len(self._items):
            self._items.pop()

        if details is None:
            details = str()

        item = RecordItem(title, deepcopy(graph), details)
        self._items.append(item)
        if not freeze_latest:
            self._latest = len(self._items)
        return item

    def load_history(self, index: int, *, freeze_latest=False) -> Graph:
        if index < 0:
            index += len(self._items)

        assert 0 <= index < len(self._items)
        item = self._items[index]
        if not freeze_latest:
            self._latest = index + 1
        return deepcopy(item.graph)

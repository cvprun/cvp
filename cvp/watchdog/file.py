# -*- coding: utf-8 -*-

from typing import List, Optional, Type

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers.api import ObservedWatch

from cvp.msgs.msg_queue import MsgQueue
from cvp.types.override import override
from cvp.watchdog.dispatcher import WatchdogEventDispatcher


class FileEventDispatcher(FileSystemEventHandler):
    def __init__(
        self,
        msgs: MsgQueue,
        file: str,
        *,
        recursive=False,
        filters: Optional[List[Type[FileSystemEvent]]] = None,
        watcher: Optional[ObservedWatch] = None,
    ):
        self._dispatcher = WatchdogEventDispatcher(msgs)
        self._file = file
        self._recursive = recursive
        self._filters = filters
        self._watcher = watcher

    @property
    def file(self):
        return self._file

    @property
    def recursive(self):
        return self._recursive

    @property
    def filters(self):
        return self._filters

    @property
    def watcher(self):
        return self._watcher

    @watcher.setter
    def watcher(self, value: Optional[ObservedWatch]) -> None:
        self._watcher = value

    def __str__(self):
        return self._file

    @override
    def on_any_event(self, event: FileSystemEvent) -> None:
        self._dispatcher.send_event(event)

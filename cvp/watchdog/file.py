# -*- coding: utf-8 -*-

from typing import List, Optional, Type, Union
from weakref import ReferenceType, ref

from cvp.msgs.msg_queue import MsgQueue
from cvp.types.override import override
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileClosedEvent,
    FileClosedNoWriteEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileOpenedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers.api import ObservedWatch


class FileEventDispatcher(FileSystemEventHandler):
    _msgs: ReferenceType[MsgQueue]

    def __init__(
        self,
        msgs: MsgQueue,
        file: str,
        *,
        recursive=False,
        filters: Optional[List[Type[FileSystemEvent]]] = None,
        watcher: Optional[ObservedWatch] = None,
    ):
        self._msgs = ref(msgs)
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

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError(f"Expired {type(self._msgs).__name__} object")
        return result

    @override
    def on_any_event(self, event: FileSystemEvent) -> None:
        pass

    @override
    def on_moved(self, event: Union[DirMovedEvent, FileMovedEvent]) -> None:
        self.msgs.file_moved(self._file)

    @override
    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        self.msgs.file_created(self._file)

    @override
    def on_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> None:
        self.msgs.file_deleted(self._file)

    @override
    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        self.msgs.file_modified(self._file)

    @override
    def on_closed(self, event: FileClosedEvent) -> None:
        self.msgs.file_closed(self._file)

    @override
    def on_closed_no_write(self, event: FileClosedNoWriteEvent) -> None:
        self.msgs.file_closed_no_write(self._file)

    @override
    def on_opened(self, event: FileOpenedEvent) -> None:
        self.msgs.file_opened(self._file)

# -*- coding: utf-8 -*-

from typing import Dict, Union
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
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch


class WatchdogManager(FileSystemEventHandler):
    _msgs: ReferenceType[MsgQueue]
    _watchers: Dict[str, ObservedWatch]

    def __init__(self, msgs: MsgQueue):
        self._msgs = ref(msgs)
        self._watchers = dict()
        self._observer = Observer()

    @property
    def watchers(self):
        return self._watchers

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError(f"Expired {type(self._msgs).__name__} object")
        return result

    def add_file(self, file: str, *, recursive=False) -> ObservedWatch:
        if file in self._watchers:
            raise KeyError(f"File already watched: '{file}'")
        watch = self._observer.schedule(self, file, recursive=recursive)
        self._watchers[file] = watch
        return watch

    def pop_file(self, file: str) -> ObservedWatch:
        if file not in self._watchers:
            raise KeyError(f"File not watched: '{file}'")
        watch = self._watchers.pop(file)
        self._observer.unschedule(watch)
        return watch

    @override
    def on_any_event(self, event: FileSystemEvent) -> None:
        pass

    @override
    def on_moved(self, event: Union[DirMovedEvent, FileMovedEvent]) -> None:
        pass

    @override
    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        pass

    @override
    def on_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> None:
        pass

    @override
    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        pass

    @override
    def on_closed(self, event: FileClosedEvent) -> None:
        pass

    @override
    def on_closed_no_write(self, event: FileClosedNoWriteEvent) -> None:
        pass

    @override
    def on_opened(self, event: FileOpenedEvent) -> None:
        pass

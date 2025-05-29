# -*- coding: utf-8 -*-

from typing import NamedTuple, Union
from weakref import ReferenceType, ref

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

from cvp.msgs.msg_queue import MsgQueue
from cvp.types.override import override


class WatchdogEventDispatcher(FileSystemEventHandler):
    _msgs: ReferenceType[MsgQueue]

    def __init__(self, msgs: MsgQueue, *, encoding="utf-8", strict="error"):
        self._msgs = ref(msgs)
        self._encoding = encoding
        self._strict = strict

    def __hash__(self):
        return hash(tuple((self.__class__, self._msgs, self._encoding, self._strict)))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (
            self._msgs == other._msgs
            and self._encoding == other._encoding
            and self._strict == other._strict
        )

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

    class _MsgArgs(NamedTuple):
        srd: str
        dest: str
        isdir: bool

    def normalize_file_system_event(self, event: FileSystemEvent) -> _MsgArgs:
        if isinstance(event.src_path, bytes):
            src = event.src_path.decode(encoding=self._encoding, errors=self._strict)
        else:
            src = event.src_path
        assert isinstance(src, str)

        if isinstance(event.dest_path, bytes):
            dest = event.dest_path.decode(encoding=self._encoding, errors=self._strict)
        else:
            dest = event.dest_path
        assert isinstance(dest, str)

        return self._MsgArgs(src, dest, event.is_directory)

    @override
    def on_moved(self, event: Union[DirMovedEvent, FileMovedEvent]) -> None:
        self.msgs.file_moved(*self.normalize_file_system_event(event))

    @override
    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        self.msgs.file_created(*self.normalize_file_system_event(event))

    @override
    def on_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> None:
        self.msgs.file_deleted(*self.normalize_file_system_event(event))

    @override
    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        self.msgs.file_modified(*self.normalize_file_system_event(event))

    @override
    def on_closed(self, event: FileClosedEvent) -> None:
        self.msgs.file_closed(*self.normalize_file_system_event(event))

    @override
    def on_closed_no_write(self, event: FileClosedNoWriteEvent) -> None:
        self.msgs.file_closed_no_write(*self.normalize_file_system_event(event))

    @override
    def on_opened(self, event: FileOpenedEvent) -> None:
        self.msgs.file_opened(*self.normalize_file_system_event(event))

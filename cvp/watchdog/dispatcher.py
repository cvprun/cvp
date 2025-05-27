# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Tuple, Union
from weakref import ReferenceType, ref

from watchdog.events import (
    EVENT_TYPE_CLOSED,
    EVENT_TYPE_CLOSED_NO_WRITE,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_MODIFIED,
    EVENT_TYPE_MOVED,
    EVENT_TYPE_OPENED,
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
)

from cvp.msgs.msg import Msg
from cvp.msgs.msg_queue import MsgQueue


class WatchdogEventDispatcher:
    _msgs: ReferenceType[MsgQueue]
    _mapping: Dict[str, Callable[[Any], Msg]]

    def __init__(self, msgs: MsgQueue, *, encoding="utf-8", strict="error"):
        self._msgs = ref(msgs)
        self._encoding = encoding
        self._strict = strict
        self._mapping = {
            EVENT_TYPE_MOVED: self.send_moved,
            EVENT_TYPE_DELETED: self.send_moved,
            EVENT_TYPE_CREATED: self.send_moved,
            EVENT_TYPE_MODIFIED: self.send_moved,
            EVENT_TYPE_CLOSED: self.send_moved,
            EVENT_TYPE_CLOSED_NO_WRITE: self.send_moved,
            EVENT_TYPE_OPENED: self.send_moved,
        }

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

    def normalize_file_system_event(
        self,
        event: FileSystemEvent,
    ) -> Tuple[str, str, bool]:
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

        return src, dest, event.is_directory

    def send_event(self, event: FileSystemEvent) -> Msg:
        return self._mapping[event.event_type](event)

    def send_moved(self, event: Union[DirMovedEvent, FileMovedEvent]) -> Msg:
        return self.msgs.file_moved(*self.normalize_file_system_event(event))

    def send_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> Msg:
        return self.msgs.file_created(*self.normalize_file_system_event(event))

    def send_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> Msg:
        return self.msgs.file_deleted(*self.normalize_file_system_event(event))

    def send_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> Msg:
        return self.msgs.file_modified(*self.normalize_file_system_event(event))

    def send_closed(self, event: FileClosedEvent) -> Msg:
        return self.msgs.file_closed(*self.normalize_file_system_event(event))

    def send_closed_no_write(self, event: FileClosedNoWriteEvent) -> Msg:
        return self.msgs.file_closed_no_write(*self.normalize_file_system_event(event))

    def send_opened(self, event: FileOpenedEvent) -> Msg:
        return self.msgs.file_opened(*self.normalize_file_system_event(event))

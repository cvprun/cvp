# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, Final, List, NewType, Optional, Sequence, Type
from uuid import uuid4

from type_serialize import Serializable
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
    FileSystemMovedEvent,
)
from watchdog.observers.api import ObservedWatch

from cvp.types.override import override
from cvp.watchdog.dispatcher import WatchdogEventDispatcher

WatchdogKey = NewType("WatchdogKey", str)


class WatchdogItem(Serializable):
    EVENT_FILTERS: Final[Sequence[Type[FileSystemEvent]]] = (
        FileSystemMovedEvent,
        FileDeletedEvent,
        FileModifiedEvent,
        FileCreatedEvent,
        FileMovedEvent,
        FileClosedEvent,
        FileClosedNoWriteEvent,
        FileOpenedEvent,
        DirDeletedEvent,
        DirModifiedEvent,
        DirCreatedEvent,
        DirMovedEvent,
    )

    _dispatcher: Optional[WatchdogEventDispatcher]
    _watcher: Optional[ObservedWatch]

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = auto()
        file = auto()
        recursive = auto()
        filters = auto()
        enabled = auto()
        managed = auto()

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        file: Optional[str] = None,
        recursive=False,
        filters: Optional[List[Type[FileSystemEvent]]] = None,
        enabled=False,
        managed=False,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.file = file if file else str()
        self.recursive = recursive
        self.filters = set(filters or ())
        self.enabled = enabled
        self.managed = managed
        self._dispatcher = None
        self._watcher = None

    @property
    def has_watcher(self) -> bool:
        if self._watcher is not None:
            assert self._dispatcher is not None
            return True
        else:
            assert self._dispatcher is None
            return False

    @staticmethod
    def filter_names_to_types(value: List[str]) -> List[Type[FileSystemEvent]]:
        from watchdog import events

        result = list()
        for name in value or ():
            filter_type = getattr(events, name, None)
            if filter_type is None:
                continue
            if not isinstance(filter_type, type):
                continue
            if not issubclass(filter_type, FileSystemEvent):
                continue
            result.append(filter_type)
        return result

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.file == other.file
            and self.recursive == other.recursive
            and self.filters == other.filters
            and self.enabled == other.enabled
            and self.managed == other.managed
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.file = copy(self.file)
        result.recursive = copy(self.recursive)
        result.filters = copy(self.filters)
        result.enabled = copy(self.enabled)
        result.managed = copy(self.managed)
        result._dispatcher = None  # dispatcher cannot be copied.
        result._watcher = None  # watcher cannot be copied.
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.file = deepcopy(self.file, memo)
        result.recursive = deepcopy(self.recursive, memo)
        result.filters = deepcopy(self.filters, memo)
        result.enabled = deepcopy(self.enabled, memo)
        result.managed = deepcopy(self.managed, memo)
        result._dispatcher = None  # dispatcher cannot be copied.
        result._watcher = None  # watcher cannot be copied.
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.uuid): self.uuid,
            str(self._Keys.name_): self.name,
            str(self._Keys.file): self.file,
            str(self._Keys.recursive): self.recursive,
            str(self._Keys.filters): self.filter_names,
            str(self._Keys.enabled): self.enabled,
            str(self._Keys.managed): self.managed,
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = str(data.get(self._Keys.uuid, str()))
        self.name = str(data.get(self._Keys.name_, str()))
        self.file = str(data.get(self._Keys.file, str()))
        self.recursive = bool(data.get(self._Keys.recursive, False))

        filter_names = data.get(self._Keys.filters, list())
        self.filters = set(self.filter_names_to_types(filter_names))

        self.enabled = bool(data.get(self._Keys.enabled, False))
        self.managed = bool(data.get(self._Keys.managed, False))

        self._dispatcher = None
        self._watcher = None

    @property
    def key(self):
        return WatchdogKey(self.uuid)

    @key.setter
    def key(self, value: WatchdogKey) -> None:
        self.uuid = str(value)

    @property
    def dispatcher(self):
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, value: Optional[WatchdogEventDispatcher]) -> None:
        self._dispatcher = value

    @property
    def watcher(self):
        return self._watcher

    @watcher.setter
    def watcher(self, value: Optional[ObservedWatch]) -> None:
        self._watcher = value

    @property
    def filter_names(self) -> List[str]:
        return [f.__name__ for f in self.filters or ()]

    @filter_names.setter
    def filter_names(self, value: List[str]) -> None:
        self.filters = set(self.filter_names_to_types(value))

    def has_event_filter(self, event_type: Type[FileSystemEvent]) -> bool:
        assert event_type in self.EVENT_FILTERS
        return event_type in self.filters

    def add_event_filter(self, event_type: Type[FileSystemEvent]) -> None:
        assert event_type in self.EVENT_FILTERS
        self.filters.add(event_type)

    def remove_event_filter(self, event_type: Type[FileSystemEvent]) -> None:
        assert event_type in self.EVENT_FILTERS
        try:
            self.filters.remove(event_type)
        except KeyError:
            pass

    def add_all_event_filters(self) -> None:
        for event_type in self.EVENT_FILTERS:
            self.filters.add(event_type)

    def clear_event_filter(self) -> None:
        self.filters.clear()

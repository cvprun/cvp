# -*- coding: utf-8 -*-

from typing import Dict

from cvp.watchdog.file import FileEventDispatcher
from watchdog.observers import Observer


class WatchdogManager(Dict[str, FileEventDispatcher]):
    def __init__(self):
        super().__init__()
        self._observer = Observer()

    def schedule_file_event(self, event: FileEventDispatcher) -> None:
        if event.watcher is not None:
            raise ValueError("Event already has a watcher")

        if self.__contains__(event.file):
            raise KeyError(f"File already watched: '{event.file}'")

        event.watcher = self._observer.schedule(
            event_handler=self,
            path=event.file,
            recursive=event.recursive,
            event_filter=event.filters,
        )
        self.__setitem__(event.file, event)

    def unschedule_file_event(
        self,
        file: str,
        *,
        no_clear_watcher=False,
    ) -> FileEventDispatcher:
        if not self.__contains__(file):
            raise KeyError(f"File not watched: '{file}'")

        event = self.pop(file)
        assert event.watcher is not None

        try:
            self._observer.unschedule(event.watcher)
        finally:
            if not no_clear_watcher:
                event.watcher = None

        return event

    def unschedule_all_file_events(self, *, no_clear_watcher=True) -> None:
        files = list(self.keys())
        for file in files:
            self.unschedule_file_event(file, no_clear_watcher=no_clear_watcher)
        assert 0 == self.__len__()

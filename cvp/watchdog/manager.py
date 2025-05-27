# -*- coding: utf-8 -*-

from typing import Dict, Optional

from watchdog.observers import Observer

from cvp.watchdog.file import FileEventDispatcher


class WatchdogManager(Dict[str, FileEventDispatcher]):
    def __init__(self, *, no_start=False, thread_name: Optional[str] = None):
        super().__init__()
        self._observer = Observer()
        self._observer.name = thread_name if thread_name else type(self).__name__
        if not no_start:
            self._observer.start()

    def start(self) -> None:
        self._observer.start()

    def stop(self) -> None:
        self._observer.stop()

    def join(self, timeout: Optional[float] = None) -> None:
        self._observer.join(timeout)

    def is_alive(self) -> bool:
        return self._observer.is_alive()

    @property
    def daemon(self) -> bool:
        return self._observer.daemon

    @property
    def ident(self) -> Optional[int]:
        return self._observer.ident

    @property
    def name(self) -> str:
        return self._observer.name

    def schedule_file_event(self, event: FileEventDispatcher) -> None:
        if event.watcher is not None:
            raise ValueError("Event already has a watcher")

        if self.__contains__(event.file):
            raise KeyError(f"File already watched: '{event.file}'")

        event.watcher = self._observer.schedule(
            event_handler=event,
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
        for file in list(self.keys()):
            self.unschedule_file_event(file, no_clear_watcher=no_clear_watcher)
        assert 0 == self.__len__()

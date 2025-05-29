# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4
from weakref import ReferenceType, ref

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from cvp.logging.loggers import watchdog_logger as logger
from cvp.msgs.msg_queue import MsgQueue
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.watchdog import WatchdogPath
from cvp.variables import WATCHDOG_NONAME
from cvp.watchdog.dispatcher import WatchdogEventDispatcher
from cvp.watchdog.item import WatchdogItem, WatchdogKey


class WatchdogManager(ResourceManager[WatchdogKey, WatchdogItem]):
    _msgs: ReferenceType[MsgQueue]
    _observer: Optional[BaseObserver]

    def __init__(
        self,
        msgs: MsgQueue,
        path: WatchdogPath,
        *,
        reload=False,
        raise_errors=False,
        autostart=False,
        thread_name: Optional[str] = None,
        encoding="utf-8",
        strict="error",
    ):
        super().__init__(
            key_type=WatchdogKey,
            config_type=WatchdogItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._msgs = ref(msgs)
        self._watchdog_path = path

        self._observer = None
        self._thread_name = thread_name if thread_name else type(self).__name__
        self._encoding = encoding
        self._strict = strict

        if autostart:
            self.open()
            self.start()
            self.schedule_all(raise_errors=raise_errors)

    @property
    def observer(self) -> BaseObserver:
        if self._observer is None:
            raise ValueError("Observer has not been started")
        return self._observer

    def open(self) -> None:
        if self._observer is not None:
            raise ValueError("Observer has already been opened")

        self._observer = Observer()
        self._observer.name = self._thread_name

    def close(self) -> None:
        if self._observer is None:
            raise ValueError("Observer has not been opened")

        if self._observer.is_alive():
            raise ValueError("Observer is still running. Stop it before closing.")

        self._observer = None

    def start(self) -> None:
        self.observer.start()

    def stop(self) -> None:
        self.observer.stop()

    def join(self, timeout: Optional[float] = None) -> None:
        self.observer.join(timeout)

    def is_alive(self) -> bool:
        return self.observer.is_alive()

    @property
    def daemon(self) -> bool:
        return self.observer.daemon

    @property
    def ident(self) -> Optional[int]:
        return self.observer.ident

    @property
    def name(self) -> str:
        return self.observer.name

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

    def add_watchdog(
        self,
        name=WATCHDOG_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[WatchdogKey, WatchdogItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = WatchdogItem(uuid=uuid, name=name)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

    def schedule(self, key: WatchdogKey) -> None:
        item = self.__getitem__(key)

        if item.dispatcher is not None:
            raise ValueError(f"'{key}' already has a dispatcher")
        if item.watcher is not None:
            raise ValueError(f"'{key}' already has a watcher")
        if not item.file:
            raise ValueError(f"'{key}' has no file path to watch")

        try:
            item.dispatcher = WatchdogEventDispatcher(
                self.msgs,
                encoding=self._encoding,
                strict=self._strict,
            )
            item.watcher = self.observer.schedule(
                event_handler=item.dispatcher,
                path=item.file,
                recursive=item.recursive,
                event_filter=item.filters or None,
            )
        except:  # noqa
            item.dispatcher = None
            item.watcher = None
            raise

    def unschedule(self, key: WatchdogKey, *, no_clear=False) -> None:
        item = self.__getitem__(key)

        if item.watcher is None:
            assert item.dispatcher is None
            raise ValueError(f"No watcher is scheduled for '{key}'")

        assert item.dispatcher is not None
        self.observer.unschedule(item.watcher)

        if not no_clear:
            item.watcher = None
            item.dispatcher = None

    def schedule_all(self, *, raise_errors=False) -> None:
        for key, item in self.items():
            if item.has_watcher:
                continue
            try:
                self.schedule(key)
            except BaseException as e:
                if raise_errors:
                    raise
                logger.error(f"Failed to schedule '{key}' - reason: '{e}'")

    def unschedule_all(self, *, raise_errors=False, no_clear=True) -> None:
        for key in self.keys():
            try:
                self.unschedule(key, no_clear=no_clear)
            except BaseException as e:
                if raise_errors:
                    raise
                logger.error(f"Failed to unschedule '{key}' - reason: '{e}'")

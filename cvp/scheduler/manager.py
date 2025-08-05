# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Tuple
from uuid import uuid4
from weakref import ReferenceType, ref

from cvp.msgs.msg_queue import MsgQueue
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.jobs import JobsPath
from cvp.scheduler.item import JobItem, JobKey
from cvp.scheduler.thread import SchedulerThread, SchedulerThreadInterface
from cvp.types.override import override
from cvp.variables import JOB_NONAME


class Scheduler(ResourceManager[JobKey, JobItem], SchedulerThreadInterface):
    _msgs: ReferenceType[MsgQueue]

    def __init__(
        self,
        path: JobsPath,
        msgs: MsgQueue,
        *,
        reload=False,
        raise_errors=False,
        autostart=False,
        thread_name: Optional[str] = None,
    ):
        super().__init__(
            key_type=JobKey,
            config_type=JobItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._msgs = ref(msgs)
        self._thread = SchedulerThread(self, name=thread_name)

        if autostart:
            self.open()
            self.start()
            self.schedule_all(raise_errors=raise_errors)

    def is_done(self) -> bool:
        return self._thread.is_done()

    @property
    def opened(self) -> bool:
        return self._thread.opened

    def open(self) -> None:
        self._thread.open()

    def close(self) -> None:
        self._thread.close()

    def start(self) -> None:
        self._thread.start()

    def start_safe(self, timeout: Optional[float] = None) -> None:
        self._thread.start_safe(timeout)

    def stop(self, *, no_clear=False) -> None:
        self._thread.stop(no_clear=no_clear)

    def clear(self) -> None:
        self._thread.clear()

    def is_scheduled(self, key: JobKey) -> bool:
        return self._thread.__contains__(key)

    def schedule(self, key: JobKey) -> None:
        self._thread.schedule(self[key])

    def unschedule(self, key: JobKey) -> None:
        self._thread.unschedule(key)

    def schedule_all(self, *, raise_errors=False) -> None:
        self._thread.schedule_all(
            filter(lambda x: x.enabled, self.values()),
            raise_errors=raise_errors,
        )

    def unschedule_all(self) -> None:
        self._thread.unschedule_all()

    def join(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

    @override
    def on_schedule_triggered(self, key: JobKey, scheduled: datetime) -> None:
        self.msgs.job_scheduled(key, scheduled)

    @override
    def on_schedule_completed(self, key: JobKey) -> None:
        self.msgs.job_completed(key)

    def add_job(
        self,
        name=JOB_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[JobKey, JobItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = JobItem(uuid=uuid, name=name)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

    def write_unmanaged_config_files(self, *, raise_errors=False) -> None:
        def _filter(__key: JobKey, __config: JobItem) -> bool:
            return not __config.managed

        self.write_all_config_files(raise_errors=raise_errors, filtering=_filter)

# -*- coding: utf-8 -*-

from copy import deepcopy
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
        no_clear=False,
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
        self._thread = SchedulerThread(self.on_scheduled, name=thread_name)

        if autostart:
            self.open()
            self.start()
            self.schedule_all(no_clear=no_clear)

    def clear(self) -> None:
        self._thread.clear()

    def schedule(self, key: JobKey, *, no_clear=False) -> None:
        self._thread.schedule(deepcopy(self[key]), no_clear=no_clear)

    def unschedule(self, key: JobKey) -> None:
        self._thread.unschedule(key)

    def schedule_all(self, *, no_clear=False) -> None:
        jobs = [deepcopy(job) for job in self.values()]
        self._thread.schedule_all(jobs, no_clear=no_clear)

    def unschedule_all(self) -> None:
        self._thread.unschedule_all()

    def quit(self) -> None:
        self._thread.quit()

    def is_done(self) -> bool:
        return self._thread.is_done()

    @property
    def opened(self) -> bool:
        return self._thread.opened

    def open(self) -> None:
        self._thread.open()

    def close(self) -> None:
        self._thread.close()

    def start_safe(self, timeout: Optional[float] = None) -> None:
        self._thread.start_safe(timeout)

    def start(self) -> None:
        self._thread.start()

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
    def on_scheduled(self, key: JobKey, scheduled: datetime) -> None:
        self.msgs.job_scheduled(key, scheduled)

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

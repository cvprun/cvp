# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from threading import Condition, RLock, Thread
from typing import Dict, Optional, Tuple
from uuid import uuid4
from weakref import ReferenceType, ref

from cvp.msgs.msg_queue import MsgQueue
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.jobs import JobsPath
from cvp.scheduler.find import find_jobs_in_time_range, find_min_next_schedule
from cvp.scheduler.item import JobItem, JobKey
from cvp.variables import JOB_NONAME


class Scheduler(ResourceManager[JobKey, JobItem]):
    _msgs: ReferenceType[MsgQueue]
    _thread: Optional[Thread]
    _scheduled: Dict[JobKey, JobItem]

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

        self._thread_name = thread_name if thread_name else type(self).__name__
        self._thread = None
        self._lock = RLock()
        self._condition = Condition(self._lock)

        # ------------------------
        # Race Condition Variables
        self._scheduled = dict()
        self._done = False
        # ------------------------

        if autostart:
            self.open()
            self.start()
            # self.schedule_all(raise_errors=raise_errors)

    def clear(self) -> None:
        with self._condition:
            self._done = False
            self._scheduled.clear()
            self._condition.notify_all()

    def schedule(self, key: JobKey, *, no_clear=False) -> None:
        item = deepcopy(self.__getitem__(key))
        if not no_clear:
            item.clear_repeat_count()
        with self._condition:
            self._scheduled[key] = item
            self._condition.notify_all()

    def unschedule(self, key: JobKey) -> None:
        with self._condition:
            if key in self._scheduled:
                del self._scheduled[key]
            self._condition.notify_all()

    def schedule_all(self, *, no_clear=False) -> None:
        items = {key: deepcopy(val) for key, val in self.items()}
        if not no_clear:
            for item in items.values():
                item.clear_repeat_count()
        with self._condition:
            self._scheduled = items
            self._condition.notify_all()

    def unschedule_all(self) -> None:
        with self._condition:
            self._scheduled.clear()
            self._condition.notify_all()

    def quit(self) -> None:
        with self._condition:
            self._done = True
            self._condition.notify_all()

    def is_done(self) -> bool:
        with self._condition:
            result = self._done
            self._condition.notify_all()
            return result

    def wait(self, timeout: Optional[float] = None) -> bool:
        with self._condition:
            signaled = self._done
            if not signaled:
                signaled = self._condition.wait(timeout)
            return signaled

    def _runner_main(self) -> None:
        with self._condition:
            begin = datetime.now().astimezone()
            while not self._done:
                next_schedule = find_min_next_schedule(self._scheduled, begin)
                if next_schedule is not None:
                    adjusted_begin = datetime.now().astimezone()
                    # Update the reference time to ignore the delay caused during
                    # schedule calculation.

                    timeout = (next_schedule - adjusted_begin).total_seconds()
                else:
                    timeout = None

                self._condition.wait(timeout)

                end = datetime.now().astimezone()
                emits = find_jobs_in_time_range(self._scheduled, begin, end)
                begin = end

                for emit_info in emits:
                    job_key, job_schedule = emit_info
                    job = self._scheduled[job_key]
                    if job.is_done:
                        continue
                    job.increment_repeat_count()
                    self.msgs.job_scheduled(job_key, job_schedule)

    @property
    def thread(self) -> Thread:
        if self._thread is None:
            raise ValueError("Thread has not been started")
        return self._thread

    @property
    def opened(self) -> bool:
        return self._thread is not None

    def _create_thread(self) -> Thread:
        return Thread(target=self._runner_main, name=self._thread_name)

    def open(self) -> None:
        if self._thread is not None:
            raise ValueError("Thread has already been opened")

        self._thread = self._create_thread()

    def close(self) -> None:
        if self._thread is None:
            raise ValueError("Thread has not been opened")

        if self._thread.is_alive():
            raise ValueError("Thread is still running. Stop it before closing.")

        self._thread = None

    def start_safe(self, timeout: Optional[float] = None) -> None:
        if self._thread is not None:
            if self._thread.is_alive():
                with self._condition:
                    self._done = True
                    self._condition.notify_all()

                self._thread.join(timeout=timeout)

            self._thread = self._create_thread()

        assert self._thread is not None
        self._thread.start()

    def start(self) -> None:
        self.thread.start()

    def join(self, timeout: Optional[float] = None) -> None:
        self.thread.join(timeout)

    def is_alive(self) -> bool:
        if self._thread is not None:
            return self._thread.is_alive()
        else:
            return False

    @property
    def daemon(self) -> Optional[bool]:
        if self._thread is not None:
            return self._thread.daemon
        else:
            return None

    @property
    def ident(self) -> Optional[int]:
        if self._thread is not None:
            return self._thread.ident
        else:
            return None

    @property
    def name(self) -> str:
        if self._thread is not None:
            return self._thread.name
        else:
            return self._thread_name

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

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

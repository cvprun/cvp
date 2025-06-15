# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import datetime
from threading import Condition, RLock, Thread
from typing import Dict, Iterable, Optional

from cvp.logging.loggers import scheduler_logger as logger
from cvp.scheduler.find import find_jobs_in_time_range, find_min_next_schedule
from cvp.scheduler.item import JobItem, JobKey
from cvp.scheduler.state import JobState
from cvp.types.override import override


class SchedulerThreadInterface(ABC):
    @abstractmethod
    def on_schedule_triggered(self, key: JobKey, scheduled: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_schedule_completed(self, key: JobKey) -> None:
        raise NotImplementedError


class SchedulerThread(SchedulerThreadInterface):
    _thread: Optional[Thread]
    _scheduled: Dict[JobKey, JobState]

    def __init__(
        self,
        callback: Optional[SchedulerThreadInterface] = None,
        *,
        name: Optional[str] = None,
    ):
        self._callback = callback
        self._name = name if name else type(self).__name__
        self._thread = None
        self._lock = RLock()
        self._condition = Condition(self._lock)

        # ------------------------
        # Race Condition Variables
        self._scheduled = dict()
        self._done = False
        # ------------------------

    def _runner_main(self) -> None:
        with self._condition:
            begin = datetime.now().astimezone()
            while not self._done:
                end = datetime.now().astimezone()
                emits = find_jobs_in_time_range(self._scheduled, begin, end)
                begin = end

                pop_keys = set()
                for emit_info in emits:
                    job_key, job_schedule = emit_info
                    state = self._scheduled[job_key]

                    if job_key in pop_keys:
                        continue

                    state.increment_repeat_count()
                    self.on_schedule_triggered(job_key, job_schedule)

                    if state.is_done:
                        pop_keys.add(job_key)

                for pop_key in pop_keys:
                    self._scheduled.pop(pop_key)
                    self.on_schedule_completed(pop_key)

                next_schedule = find_min_next_schedule(self._scheduled, begin)
                if next_schedule is not None:
                    adjusted_begin = datetime.now().astimezone()
                    # Update the reference time to ignore the delay caused during
                    # schedule calculation.

                    timeout = (next_schedule - adjusted_begin).total_seconds()
                else:
                    timeout = None

                self._condition.wait(timeout)

    @override
    def on_schedule_triggered(self, key: JobKey, scheduled: datetime) -> None:
        if self._callback is not None:
            self._callback.on_schedule_triggered(key, scheduled)

    @override
    def on_schedule_completed(self, key: JobKey) -> None:
        if self._callback is not None:
            self._callback.on_schedule_completed(key)

    @property
    def opened(self) -> bool:
        return self._thread is not None

    def _create_thread(self) -> Thread:
        return Thread(target=self._runner_main, name=self._name, daemon=True)

    def open(self) -> None:
        if self._thread is not None:
            raise ValueError("Thread has already been opened")

        with self._condition:
            self._done = False
        self._thread = self._create_thread()

    def close(self) -> None:
        if self._thread is None:
            raise ValueError("Thread has not been opened")

        if self._thread.is_alive():
            raise ValueError("Thread is still running. Stop it before closing.")

        self._thread = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self) -> None:
        if self._thread is None:
            raise ValueError("Thread has not been started")

        self._thread.start()

    def start_safe(self, timeout: Optional[float] = None) -> None:
        if self._thread is not None:
            if self._thread.is_alive():
                with self._condition:
                    self._done = True
                    self._scheduled.clear()
                    self._condition.notify_all()

                self._thread.join(timeout=timeout)

            self._thread = self._create_thread()

        assert self._thread is not None
        with self._condition:
            self._done = False
            self._scheduled.clear()
        self._thread.start()

    def stop(self, *, no_clear=False) -> None:
        with self._condition:
            self._done = True
            if not no_clear:
                self._scheduled.clear()
            self._condition.notify_all()

    def clear(self) -> None:
        with self._condition:
            self._done = False
            self._scheduled.clear()
            self._condition.notify_all()

    def __contains__(self, key: JobKey) -> bool:
        with self._condition:
            return self._scheduled.__contains__(key)

    def get_repeat_count(self, key: JobKey) -> int:
        with self._condition:
            return self._scheduled[key].repeat_count

    def schedule(self, job: JobItem) -> None:
        state = JobState(job.cron, job.repeat)
        with self._condition:
            self._scheduled[job.key] = state
            self._condition.notify_all()

    def unschedule(self, key: JobKey) -> None:
        with self._condition:
            if key in self._scheduled:
                del self._scheduled[key]
            self._condition.notify_all()

    def schedule_all(self, jobs: Iterable[JobItem], *, raise_errors=False) -> None:
        scheduled = dict()
        for job in jobs:
            try:
                scheduled[job.key] = JobState(job.cron, job.repeat)
            except BaseException as e:
                if raise_errors:
                    raise
                logger.error(f"Failed to schedule '{job.key}' - reason: '{e}'")

        with self._condition:
            self._scheduled = scheduled
            self._condition.notify_all()

    def unschedule_all(self) -> None:
        with self._condition:
            self._scheduled.clear()
            self._condition.notify_all()

    def is_done(self) -> bool:
        with self._condition:
            result = self._done
            self._condition.notify_all()
            return result

    def join(self, timeout: Optional[float] = None) -> None:
        if self._thread is None:
            raise ValueError("Thread has not been started")

        self._thread.join(timeout)

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
            return self._name

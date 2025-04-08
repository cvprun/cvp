# -*- coding: utf-8 -*-

from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from typing import Callable, Optional, ParamSpec, TypeVar

from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.logging.logging import logger
from cvp.process.helper.ffmpeg import FFmpegProcessHelper
from cvp.process.mapper import ProcessMapper
from cvp.process.process import Process
from cvp.resources.home import HomeDir
from cvp.variables import MAX_PROCESS_WORKERS, MAX_THREAD_WORKERS, THREAD_POOL_PREFIX

SubmitResultT = TypeVar("SubmitResultT")
SubmitParamT = ParamSpec("SubmitParamT")
SubmitCallable = Callable[SubmitParamT, SubmitResultT]


class ProcessManager:
    def __init__(
        self,
        config: FFmpegConfig,
        home: HomeDir,
        thread_workers=MAX_THREAD_WORKERS,
        thread_name_prefix=THREAD_POOL_PREFIX,
        process_workers=MAX_PROCESS_WORKERS,
    ):
        if thread_workers < 1:
            raise ValueError("The 'thread_workers' argument must be at least 2")
        if process_workers < 1:
            raise ValueError("The 'process_workers' argument must be at least 2")

        logger.info(f"Create ThreadPoolExecutor(max_workers={thread_workers}) of PM")
        self._thread_pool = ThreadPoolExecutor(
            max_workers=thread_workers,
            thread_name_prefix=thread_name_prefix,
        )

        logger.info(f"Create ProcessPoolExecutor(max_workers={process_workers}) of PM")
        self._process_pool = ProcessPoolExecutor(max_workers=process_workers)

        self._processes = ProcessMapper[str, Process]()
        self._ffmpeg = FFmpegProcessHelper(config=config, home=home)

    @property
    def thread_pool(self):
        return self._thread_pool

    @property
    def process_pool(self):
        return self._process_pool

    @property
    def processes(self):
        return self._processes

    def submit_thread(
        self,
        fn: Callable[SubmitParamT, SubmitResultT],
        *args: SubmitParamT.args,
        **kwargs: SubmitParamT.kwargs,
    ) -> Future[SubmitResultT]:
        return self._thread_pool.submit(fn, *args, **kwargs)

    def submit_process(
        self,
        fn: Callable[SubmitParamT, SubmitResultT],
        *args: SubmitParamT.args,
        **kwargs: SubmitParamT.kwargs,
    ) -> Future[SubmitResultT]:
        return self._process_pool.submit(fn, *args, **kwargs)

    def keys(self):
        return self._processes.keys()

    def values(self):
        return self._processes.values()

    def items(self):
        return self._processes.items()

    def spawnable(self, key: str):
        return self._processes.spawnable(key)

    def stoppable(self, key: str):
        return self._processes.stoppable(key)

    def removable(self, key: str):
        return self._processes.removable(key)

    def status(self, key: str):
        return self._processes.status(key)

    def interrupt(self, key: str):
        return self._processes.interrupt(key)

    def get(self, key: str):
        return self._processes.get(key)

    def pop(self, key: str):
        if not self._processes.removable(key):
            raise ValueError(f"Non-removable process: '{key}'")

        process = self._processes.pop(key)
        process.teardown()
        return process

    def teardown(self, timeout: Optional[float] = None):
        logger.info("ProcessManager is terminating all processes ...")

        processes = list()
        while self._processes:
            processes.append(self._processes.popitem()[1])

        for proc in processes:
            if proc.poll() is not None:
                continue

            logger.info(f"Interrupt the process ({proc.pid}) ...")
            proc.interrupt()

        timeout_logging = f" (timeout={timeout:.03f}s)" if timeout is not None else ""
        for proc in processes:
            try:
                logger.info(f"Waiting the process ({proc.pid}) ...{timeout_logging}")
                proc.wait(timeout)
            except TimeoutError:
                logger.warning(f"Timeout raised! KILL process ({proc.pid})")
                proc.kill()

        for proc in processes:
            logger.info(f"Calls the teardown callback of process {proc.pid}")
            proc.teardown()

        for proc in processes:
            logger.info(f"The exit code of process ({proc.pid}) is {proc.returncode}")

        logger.info("Shutting down PM's thread pool...")
        self._thread_pool.shutdown(wait=True)

        logger.info("Shutting down PM's process pool...")
        self._process_pool.shutdown(wait=True)

    def spawn_ffmpeg_with_file(self, key: str, file: str, width: int, height: int):
        if key in self._processes:
            raise KeyError(f"Key is exists: '{key}'")

        process = self._ffmpeg.spawn_with_file(key, file, width, height)
        self._processes[key] = process
        return process

    def create_thread_runner(
        self,
        callback: SubmitCallable,
    ) -> ThreadRunnable[SubmitParamT, SubmitResultT]:
        return ThreadRunnable(self._thread_pool, callback)

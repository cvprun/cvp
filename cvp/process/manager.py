# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.logging.logging import logger
from cvp.process.helper.ffmpeg import FFmpegProcessHelper
from cvp.process.mapper import ProcessMapper
from cvp.process.process import Process
from cvp.resources.home import HomeDir


class ProcessManager:
    def __init__(
        self,
        config: FFmpegConfig,
        home: HomeDir,
    ):
        self._processes = ProcessMapper[str, Process]()
        self._ffmpeg = FFmpegProcessHelper(config=config, home=home)

    @property
    def processes(self):
        return self._processes

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

    def spawn_ffmpeg_with_file(self, key: str, file: str, width: int, height: int):
        if key in self._processes:
            raise KeyError(f"Key is exists: '{key}'")

        process = self._ffmpeg.spawn_with_file(key, file, width, height)
        self._processes[key] = process
        return process

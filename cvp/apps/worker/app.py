# -*- coding: utf-8 -*-

from asyncio import get_running_loop, sleep
from multiprocessing.queues import Queue
from typing import Optional

from cvp.aio.run import aio_run
from cvp.logging.loggers import worker_logger as logger
from cvp.variables import LOGGING_STEP, SLOW_CALLBACK_DURATION


class WorkerApplication:
    def __init__(
        self,
        *args,
        queue: Optional[Queue] = None,
        logging_step=LOGGING_STEP,
        slow_callback_duration=SLOW_CALLBACK_DURATION,
        use_uvloop=False,
        debug=False,
        verbose=0,
    ):
        self._args = args
        self._queue = queue
        self._logging_step = logging_step
        self._slow_callback_duration = slow_callback_duration
        self._use_uvloop = use_uvloop
        self._debug = debug
        self._verbose = verbose

    async def on_main(self):
        logger.debug(f"Initial arguments: {self._args}")

        loop = get_running_loop()
        loop.slow_callback_duration = self._slow_callback_duration
        loop.set_debug(self._debug)

        try:
            while True:
                await sleep(1.0)
        finally:
            if self._queue is not None:
                self._queue.cancel_join_thread()

    def start(self) -> None:
        try:
            aio_run(self.on_main(), self._use_uvloop)
        except (KeyboardInterrupt, InterruptedError):
            logger.warning("An interrupt signal was detected")

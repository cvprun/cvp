# -*- coding: utf-8 -*-

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, Generic, Optional, ParamSpec, TypeVar
from weakref import ref

from cvp.logging.loggers import logger

_P = ParamSpec("_P")
_T = TypeVar("_T")


class ThreadRunnable(Generic[_P, _T]):
    _future: Optional[Future[_T]]
    _result: Optional[_T]
    _error: Optional[BaseException]

    def __init__(
        self,
        executor: ThreadPoolExecutor,
        callback: Callable[_P, _T],
    ):
        self._executor = ref(executor)
        self._callback = callback

        self._running = False
        self._future = None
        self._result = None
        self._error = None

    def clear(self) -> None:
        self._running = False
        self._future = None
        self._result = None
        self._error = None

    @property
    def running(self):
        if not self._running:
            return False
        assert self._future is not None
        return self._future.running()

    @property
    def future(self):
        return self._future

    @property
    def result(self):
        return self._result

    @property
    def error(self):
        return self._error

    def __bool__(self):
        return self.running

    def cancel(self) -> bool:
        if not self._running:
            raise ValueError("Not running")
        assert self._future is not None
        return self._future.cancel()

    def _runner(self, *args: _P.args, **kwargs: _P.kwargs):
        assert self._running
        assert self._result is None
        assert self._error is None

        try:
            self._result = self._callback(*args, **kwargs)
            return self._result
        except BaseException as e:
            self._error = e
            logger.exception(e)
        finally:
            self._running = False

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs):
        if self._running:
            raise ValueError("Now running. Cannot be run repeatedly.")

        executor = self._executor()
        if executor is None:
            raise ReferenceError("The executor object has expired")

        assert isinstance(executor, ThreadPoolExecutor)

        self._running = True
        self._result = None
        self._error = None
        self._future = executor.submit(self._runner, *args, **kwargs)
        return self._future

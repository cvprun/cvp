# -*- coding: utf-8 -*-

from concurrent.futures import Future
from typing import Callable, ParamSpec, TypeVar

from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.context.mixins.protocol import ContextProtocol

SubmitResultT = TypeVar("SubmitResultT")
SubmitParamT = ParamSpec("SubmitParamT")


class BaseContextMixin(ContextProtocol):
    def submit_thread(
        self,
        fn: Callable[SubmitParamT, SubmitResultT],
        *args: SubmitParamT.args,
        **kwargs: SubmitParamT.kwargs,
    ) -> Future[SubmitResultT]:
        return self._thread_pool.submit(fn, *args, **kwargs)

    def create_thread_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        return ThreadRunnable[SubmitParamT, SubmitResultT](self._thread_pool, callback)

    def get_thread_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        property_prefix = str(callback.__name__)
        property_suffix = ThreadRunnable.__name__
        property_name = f"{property_prefix}.{property_suffix}"
        runner = getattr(self, property_name, None)

        if runner is None:
            runner = self.create_thread_runner(callback)
            setattr(self, property_name, runner)

        assert runner is not None
        return runner

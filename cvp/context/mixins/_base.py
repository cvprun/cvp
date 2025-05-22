# -*- coding: utf-8 -*-

from concurrent.futures import Future
from typing import Callable, ParamSpec, TypeVar

from cvp.concurrency.threading.runnable import ConcurrencyRunnable
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

    def submit_process(
        self,
        fn: Callable[SubmitParamT, SubmitResultT],
        *args: SubmitParamT.args,
        **kwargs: SubmitParamT.kwargs,
    ) -> Future[SubmitResultT]:
        return self._process_pool.submit(fn, *args, **kwargs)

    def create_thread_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        return ConcurrencyRunnable[SubmitParamT, SubmitResultT](
            executor=self._thread_pool,
            callback=callback,
        )

    def create_process_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        return ConcurrencyRunnable[SubmitParamT, SubmitResultT](
            executor=self._process_pool,
            callback=callback,
        )

    def get_thread_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        property_prefix = str(callback.__name__)
        property_middle = ConcurrencyRunnable.__name__
        property_suffix = self.get_thread_runner.__name__
        property_name = f"{property_prefix}.{property_middle}.{property_suffix}"
        runner = getattr(self, property_name, None)

        if runner is None:
            runner = self.create_thread_runner(callback)
            setattr(self, property_name, runner)

        assert runner is not None
        assert runner.is_thread_pool_runner
        return runner

    def get_process_runner(self, callback: Callable[SubmitParamT, SubmitResultT]):
        property_prefix = str(callback.__name__)
        property_middle = ConcurrencyRunnable.__name__
        property_suffix = self.get_process_runner.__name__
        property_name = f"{property_prefix}.{property_middle}.{property_suffix}"
        runner = getattr(self, property_name, None)

        if runner is None:
            runner = self.create_process_runner(callback)
            setattr(self, property_name, runner)

        assert runner is not None
        assert runner.is_process_pool_runner
        return runner

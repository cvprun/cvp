# -*- coding: utf-8 -*-

from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from threading import Event
from typing import Callable, ParamSpec, Protocol, TypeVar, runtime_checkable

from cvp.chat.manager import ChatManager
from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.config.config import Config
from cvp.flow.manager import FlowManager
from cvp.keyring.root import RootKeyring
from cvp.msgs.msg_queue import MsgQueue
from cvp.ollama.manager import OllamaManager
from cvp.onvif.manager import OnvifManager
from cvp.resources.home import HomeDir
from cvp.supabase.supabase import Supabase
from cvp.wsdiscovery.manager import WsDiscoveryManager

SubmitResultT = TypeVar("SubmitResultT")
SubmitParamT = ParamSpec("SubmitParamT")


@runtime_checkable
class ContextProtocol(Protocol):
    _home: HomeDir
    _config: Config
    _done: Event
    _thread_pool: ThreadPoolExecutor
    _process_pool: ProcessPoolExecutor
    _keyring: RootKeyring
    _onvifs: OnvifManager
    _chat: ChatManager
    _ollamas: OllamaManager
    _flows: FlowManager
    _msg_queue: MsgQueue
    _supabase: Supabase
    _wsdiscovery: WsDiscoveryManager


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

# -*- coding: utf-8 -*-

from threading import Event
from typing import Protocol, runtime_checkable

from cvp.chat.manager import ChatManager
from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.config.config import Config
from cvp.flow.manager import FlowManager
from cvp.keyring.root import RootKeyring
from cvp.msgs.msg_queue import MsgQueue
from cvp.ollama.manager import OllamaManager
from cvp.onvif.manager import OnvifManager
from cvp.process.manager import ProcessManager, SubmitCallable
from cvp.resources.home import HomeDir
from cvp.supabase.supabase import Supabase
from cvp.wsdiscovery.manager import WsDiscoveryManager


@runtime_checkable
class ContextProtocol(Protocol):
    _home: HomeDir
    _config: Config
    _done: Event
    _process_manager: ProcessManager
    _keyring: RootKeyring
    _onvif_manager: OnvifManager
    _chat: ChatManager
    _ollamas: OllamaManager
    _flows: FlowManager
    _msg_queue: MsgQueue
    _supabase: Supabase
    _wsdiscovery: WsDiscoveryManager


class BaseContextMixin(ContextProtocol):
    def get_thread_runner(self, callback: SubmitCallable):
        property_prefix = str(callback.__name__)
        property_suffix = ThreadRunnable.__name__
        property_name = f"{property_prefix}.{property_suffix}"
        runner = getattr(self, property_name, None)

        if runner is None:
            runner = self._process_manager.create_thread_runner(callback)
            setattr(self, property_name, runner)

        assert runner is not None
        return runner

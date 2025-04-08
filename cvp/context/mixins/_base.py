# -*- coding: utf-8 -*-

from threading import Event
from typing import Protocol, runtime_checkable

from cvp.chat.manager import ChatManager
from cvp.config.config import Config
from cvp.flow.manager import FlowManager
from cvp.keyring.root import RootKeyring
from cvp.msgs.msg_queue import MsgQueue
from cvp.ollama.manager import OllamaManager
from cvp.onvif.manager import OnvifManager
from cvp.process.manager import ProcessManager
from cvp.resources.home import HomeDir
from cvp.supabase.supabase import Supabase


@runtime_checkable
class BaseContextMixin(Protocol):
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

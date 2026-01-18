# -*- coding: utf-8 -*-

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Event
from typing import Protocol, runtime_checkable

from cvp.canvas.manager import CanvasManager
from cvp.chat.manager import ChatManager
from cvp.config.config import Config
from cvp.context.hub import HubManager
from cvp.download.manager import DownloadManager
from cvp.flow.manager import FlowManager
from cvp.ime.manager import ImeManager
from cvp.keyring.root import RootKeyring
from cvp.media.manager import MediaManager
from cvp.mediamtx.manager import MediamtxManager
from cvp.msgs.msg_queue import MsgQueue
from cvp.ollama.manager import OllamaManager
from cvp.onvif.manager import OnvifManager
from cvp.resources.home import HomeDir
from cvp.scheduler.manager import Scheduler
from cvp.service.manager import ServiceManager
from cvp.supabase.supabase import Supabase
from cvp.tail.manager import TailManager
from cvp.terminal.manager import TerminalManager
from cvp.text.manager import TextManager
from cvp.watchdog.manager import WatchdogManager
from cvp.wsdiscovery.manager import WsDiscoveryManager


@runtime_checkable
class ContextProtocol(Protocol):
    _home: HomeDir
    _config: Config
    _done: Event

    _thread_pool: ThreadPoolExecutor
    _process_pool: ProcessPoolExecutor

    _keyring: RootKeyring

    _msgs: MsgQueue
    _watchdogs: WatchdogManager
    _imes: ImeManager
    _ollamas: OllamaManager
    _canvases: CanvasManager
    _chat: ChatManager
    _flows: FlowManager
    _scheduler: Scheduler
    _services: ServiceManager
    _wsdiscovery: WsDiscoveryManager
    _downloader: DownloadManager
    _onvifs: OnvifManager
    _medias: MediaManager
    _mediamtxs: MediamtxManager
    _tails: TailManager
    _terminals: TerminalManager
    _texts: TextManager
    _supabase: Supabase
    _hub: HubManager

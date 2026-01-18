# -*- coding: utf-8 -*-

import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import get_start_method
from os import PathLike
from threading import Event
from typing import Optional, Union

from cvp.canvas.manager import CanvasManager
from cvp.chat.manager import ChatManager
from cvp.config.config import Config
from cvp.context._protocol import ContextProtocol
from cvp.context.hub import HubManager
from cvp.context.mixins import ContextMixins
from cvp.download.manager import DownloadManager
from cvp.filesystem.permission import test_directory, test_readable, test_writable
from cvp.flow.graph import FlowGraph
from cvp.flow.manager import FlowManager
from cvp.flow.node import FlowNode
from cvp.flow.runner import FlowRunner
from cvp.ime.manager import ImeManager
from cvp.keyring.root import RootKeyring
from cvp.logging.loggers import logger
from cvp.logging.logging import (
    convert_level_number,
    dumps_default_logging_config,
    loads_logging_config,
    set_root_level,
)
from cvp.media.manager import MediaManager
from cvp.mediamtx.manager import MediamtxManager
from cvp.modules.warnings import hide_pkg_resources_deprecated_warning
from cvp.msgs.msg import Msg
from cvp.msgs.msg_queue import MsgQueue
from cvp.msgs.msg_type import MsgType
from cvp.ollama.manager import OllamaManager
from cvp.onvif.manager import OnvifManager
from cvp.resources.home import HomeDir
from cvp.scheduler.manager import Scheduler
from cvp.service.manager import ServiceManager
from cvp.supabase.supabase import Supabase
from cvp.system.environ_keys import PYOPENGL_USE_ACCELERATE, SDL_VIDEO_X11_FORCE_EGL
from cvp.tail.manager import TailManager
from cvp.terminal.manager import TerminalManager
from cvp.text.manager import TextManager
from cvp.watchdog.manager import WatchdogManager
from cvp.wsdiscovery.manager import WsDiscoveryManager


def _fetch_best_opengl_config():
    try:
        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.apps.tester.fetch import fetch_best_opengl_config_from_subprocess

        return fetch_best_opengl_config_from_subprocess()
    except:  # noqa
        return None


class Context(ContextMixins):
    def __init__(self, home: Union[str, PathLike[str]], *, detect_opengl=False):
        self._home = HomeDir(home)
        self._config = Config()
        self._done = Event()

        test_directory(self._home)
        test_readable(self._home)
        test_writable(self._home)

        if self._home.cvp_yml.is_file():
            self._config.read_yaml(self._home.cvp_yml)

        if not self._home.logging_json.exists():
            logging_path = str(self._home.logging_json)
            logger.info(f"Save the default logging config file: '{logging_path}'")
            logging_json_text = dumps_default_logging_config(
                cvp_home=self._home,
                logs_dirname=self._home.logs.get_subdir_name(),
            )
            self._home.logging_json.write_text(logging_json_text)

        if self._config.logging.config_path is None:
            logging_path = str(self._home.logging_json)
            logger.info(f"Initialize default logging config file: '{logging_path}'")
            self._config.logging.config_path = logging_path

        logging_config_path = self._config.logging.config_path
        assert isinstance(logging_config_path, str)

        if os.path.isfile(logging_config_path):
            loads_logging_config(logging_config_path)
            logger.info(f"Loads the logging config file: '{logging_config_path}'")

        if self._config.logging.root_severity:
            root_severity = self._config.logging.root_severity
            level = convert_level_number(root_severity)
            set_root_level(level)
            logger.log(level, f"Changed root severity: {root_severity}")

        logger.info(f"Current multiprocessing start method: {get_start_method()}")
        # [NOTE] The "multiprocessing start method" should be changed immediately after
        # importing the module, so calling it in the constructor of Context is too late.

        thread_workers = self._config.concurrency.thread_workers
        thread_name_prefix = self._config.concurrency.thread_name_prefix
        self._thread_pool = ThreadPoolExecutor(
            max_workers=thread_workers,
            thread_name_prefix=thread_name_prefix,
        )
        logger.info(f"Create ThreadPoolExecutor(max_workers={thread_workers})")

        process_workers = self._config.concurrency.process_workers
        self._process_pool = ProcessPoolExecutor(max_workers=process_workers)
        logger.info(f"Create ProcessPoolExecutor(max_workers={process_workers}) of PM")

        if detect_opengl and not self._home.cvp_yml.is_file():
            logger.warning("Detect OpenGL config via subprocess ...")
            if opengl_config := _fetch_best_opengl_config():
                logger.info(f"Force EGL: {opengl_config.force_egl}")
                logger.info(f"PyOpenGL Accelerate: {opengl_config.use_accelerate}")
                self._config.graphic.force_egl = opengl_config.force_egl
                self._config.graphic.use_accelerate = opengl_config.use_accelerate

        if self._config.graphic.force_egl is not None:
            force_egl = self._config.graphic.force_egl_environ
            os.environ[SDL_VIDEO_X11_FORCE_EGL] = force_egl
            logger.info(f"Update environ: {SDL_VIDEO_X11_FORCE_EGL}={force_egl}")

        if self._config.graphic.use_accelerate is not None:
            use_accelerate = self._config.graphic.use_accelerate_environ
            os.environ[PYOPENGL_USE_ACCELERATE] = use_accelerate
            logger.info(f"Update environ: {PYOPENGL_USE_ACCELERATE}={use_accelerate}")

        if self._config.onvif.preload:
            logger.info("Launching ONVIF service declaration preload on a new thread")
            self.preload_onvif_declarations()

        hide_pkg_resources_deprecated_warning(logger, details=self._config.debug)

        self._keyring = RootKeyring()
        if self._home.is_dir():
            logger.info(f"Default keyring directory: {str(self._home.keyrings)}")
            self._keyring.update_default_filepath(self._home.keyrings)

        self._msgs = MsgQueue()
        self._scheduler = Scheduler(
            self._home.jobs,
            self._msgs,
            reload=True,
            autostart=True,
        )
        self._watchdogs = WatchdogManager(
            self._msgs,
            self._home.watchdog,
            reload=True,
            autostart=True,
        )
        self._imes = ImeManager.from_default()
        self._ollamas = OllamaManager(self._home.ollamas, reload=True)
        self._canvases = CanvasManager(self._home.canvases, reload=True)
        self._chat = ChatManager(self._home.chat, create_tables=True, reload=True)
        self._flows = FlowManager(self._home.flows, reload=True)
        self._services = ServiceManager(
            self._home.services,
            self._home.processes,
            self._msgs,
            reload=True,
        )
        self._wsdiscovery = WsDiscoveryManager(self._home.wsdiscovery, reload=True)
        self._downloader = DownloadManager(
            self._home.downloads,
            self._home.temp.as_path(),
            reload=True,
        )

        self._onvifs = OnvifManager(self._home.onvifs, reload=True)
        self.initialize_onvif_clients()

        self._medias = MediaManager(
            self._home.medias,
            self._home.processes,
            self._config.ffmpeg,
            reload=True,
        )
        self._mediamtxs = MediamtxManager(self._home.mediamtx, reload=True)
        self._tails = TailManager(self._home.tails, reload=True)
        self._terminals = TerminalManager(self._home.terminals, reload=True)
        self._texts = TextManager(self._home.texts, reload=True)

        self._supabase = Supabase()
        if self.supabase_url and self.supabase_key:
            self.create_supabase_client(
                self.supabase_url,
                self.supabase_key,
                self.server_username,
                self.server_password,
            )

        hub_host = self._config.hub.host
        hub_port = self._config.hub.port
        self._hub = HubManager(hub_host, hub_port)
        if self._config.hub.autostart:
            self._hub.start()

        assert isinstance(self, ContextProtocol)

    def shutdown(self, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = self._config.process.teardown_timeout
        assert timeout is not None

        logger.info("Unschedule watchdog events ...")
        self._watchdogs.unschedule_all()

        if self._watchdogs.is_alive():
            logger.info("Stop watchdog thread ...")
            self._watchdogs.stop()

        logger.info(f"Join watchdog thread ... ({timeout:.02f}s)")
        self._watchdogs.join(timeout)

        if self._scheduler.is_alive():
            logger.info("Stop scheduler thread ...")
            self._scheduler.stop()

        logger.info(f"Join scheduler thread ... ({timeout:.02f}s)")
        self._scheduler.join(timeout)

        logger.info("Close message queue ...")
        self._msgs.close()

        logger.info("Join message queue ...")
        self._msgs.join_thread()

        logger.info("Stop all flow runners")
        self._flows.stop_all_runners()

        logger.info(f"Stop all media processes ... ({timeout:.02f}s)")
        self._medias.shutdown(timeout)

        logger.info(f"Stop all service processes ... ({timeout:.02f}s)")
        self._services.shutdown(timeout)

        if self._hub.is_running:
            logger.info("Stopping Hub server ...")
            self._hub.stop()

        logger.info("Shutting down thread pool ...")
        self._thread_pool.shutdown(wait=True)

        logger.info("Shutting down process pool ...")
        self._process_pool.shutdown(wait=True)

    def save_config(self) -> None:
        self._config.write_yaml(self._home.cvp_yml)
        logger.info(f"Save the Config file: '{str(self._home.cvp_yml)}'")

    def save_unmanaged_scheduler(self) -> None:
        self._scheduler.write_unmanaged_config_files()
        logger.info("Save unmanaged Schedule files")

    def save_unmanaged_watchdogs(self) -> None:
        self._watchdogs.write_unmanaged_config_files()
        logger.info("Save unmanaged Watchdog files")

    def save_all_ollamas(self) -> None:
        self._ollamas.write_all_config_files()
        logger.info("Save all Ollama files")

    def save_all_canvases(self) -> None:
        self._canvases.write_all_config_files()
        logger.info("Save all Canvas files")

    def save_unmanaged_services(self) -> None:
        self._services.write_unmanaged_config_files()
        logger.info("Save unmanaged Service files")

    def save_flow_graph(self, graph: FlowGraph) -> None:
        self._flows.write_graph_file(graph)
        logger.info(f"Save the Graph file: '{graph.key}'")

    def save_all_flow_graphs(self) -> None:
        self._flows.write_all_graph_file(raise_errors=False)
        logger.info("Save all Graph files")

    def save_all_wsdiscovery(self) -> None:
        self._wsdiscovery.write_all_config_files()
        logger.info("Save all WS-Discovery files")

    def save_all_downloader(self) -> None:
        self._downloader.write_all_config_files()
        logger.info("Save all Downloader files")

    def save_all_onvifs(self) -> None:
        self._onvifs.write_all_config_files()
        logger.info("Save all Onvif files")

    def save_all_medias(self) -> None:
        self._medias.write_all_config_files()
        logger.info("Save all Media files")

    def save_all_mediamtxs(self) -> None:
        self._mediamtxs.write_all_config_files()
        logger.info("Save all MediaMTX files")

    def save_all_tails(self) -> None:
        self._tails.write_all_config_files()
        logger.info("Save all Tail files")

    def save_all_terminals(self) -> None:
        self._terminals.write_all_config_files()
        logger.info("Save all Terminal files")

    def save_all_texts(self) -> None:
        self._texts.write_all_config_files()
        logger.info("Save all Text files")

    def save_all(self) -> None:
        self.save_config()
        self.save_unmanaged_scheduler()
        self.save_unmanaged_watchdogs()
        self.save_all_ollamas()
        self.save_all_canvases()
        self.save_unmanaged_services()
        self.save_all_flow_graphs()
        self.save_all_wsdiscovery()
        self.save_all_downloader()
        self.save_all_onvifs()
        self.save_all_medias()
        self.save_all_mediamtxs()
        self.save_all_tails()
        self.save_all_terminals()
        self.save_all_texts()

    @property
    def home(self):
        return self._home

    @property
    def config(self):
        return self._config

    @property
    def msgs(self):
        return self._msgs

    @property
    def watchdogs(self):
        return self._watchdogs

    @property
    def imes(self):
        return self._imes

    @property
    def ollamas(self):
        return self._ollamas

    @property
    def canvases(self):
        return self._canvases

    @property
    def chat(self):
        return self._chat

    @property
    def flows(self):
        return self._flows

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def services(self):
        return self._services

    @property
    def keyring(self):
        return self._keyring

    @property
    def wsdiscovery(self):
        return self._wsdiscovery

    @property
    def downloader(self):
        return self._downloader

    @property
    def onvifs(self):
        return self._onvifs

    @property
    def medias(self):
        return self._medias

    @property
    def mediamtxs(self):
        return self._mediamtxs

    @property
    def tails(self):
        return self._tails

    @property
    def terminals(self):
        return self._terminals

    @property
    def texts(self):
        return self._texts

    @property
    def supabase(self):
        return self._supabase

    @property
    def hub(self):
        return self._hub

    @property
    def debug(self) -> bool:
        return self._config.debug

    @property
    def verbose(self) -> int:
        return self._config.verbose

    def quit(self) -> None:
        self._done.set()

    def is_done(self) -> bool:
        return self._done.is_set()

    def do_msg(self, msg: Msg) -> None:
        if msg.mtype == MsgType.process_exited:
            self.handle_exited_process(msg.key)
        elif msg.mtype == MsgType.process_restart:
            self.handle_restart_process(msg.key)

    def start_flow_thread(self, graph: FlowGraph, start_node: Union[FlowNode, str]):
        runner = FlowRunner(
            executor=self._thread_pool,
            graph=graph,
            start_node=start_node,
            use_copy=False,
            use_deepcopy=False,
            debug=self.debug,
            verbose=self.verbose,
        )
        self._flows.runners[graph.key] = runner
        return runner

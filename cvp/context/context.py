# -*- coding: utf-8 -*-

import os
from os import PathLike
from threading import Event
from typing import Optional, Union

from cvp.config.config import Config
from cvp.filesystem.permission import test_directory, test_readable, test_writable
from cvp.flow.graph import FlowGraph
from cvp.flow.manager import FlowManager
from cvp.flow.node import FlowNode
from cvp.flow.runner import FlowRunner
from cvp.logging.logging import (
    convert_level_number,
    dumps_default_logging_config,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.msgs.msg_queue import MsgQueue
from cvp.onvif.manager import OnvifManager
from cvp.process.manager import ProcessManager
from cvp.resources.download.archive import DownloadArchive
from cvp.resources.download.links.tuples import LinkInfo
from cvp.resources.download.runner import DownloadRunner
from cvp.resources.home import HomeDir
from cvp.supabase.supabase import Supabase
from cvp.system.environ_keys import PYOPENGL_USE_ACCELERATE, SDL_VIDEO_X11_FORCE_EGL


class Context:
    def __init__(self, home: Union[str, PathLike[str]]):
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
            logging_json_text = dumps_default_logging_config(cvp_home=self._home)
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

        thread_workers = self._config.concurrency.thread_workers
        thread_name_prefix = self._config.concurrency.thread_name_prefix
        process_workers = self._config.concurrency.process_workers

        self._process_manager = ProcessManager(
            config=self._config.ffmpeg,
            home=self._home,
            thread_workers=thread_workers,
            thread_name_prefix=thread_name_prefix,
            process_workers=process_workers,
        )

        if self._config.graphic.force_egl is not None:
            force_egl = self._config.graphic.force_egl_environ
            os.environ[SDL_VIDEO_X11_FORCE_EGL] = force_egl
            logger.info(f"Update environ: {SDL_VIDEO_X11_FORCE_EGL}={force_egl}")

        if self._config.graphic.use_accelerate is not None:
            use_accelerate = self._config.graphic.use_accelerate_environ
            os.environ[PYOPENGL_USE_ACCELERATE] = use_accelerate
            logger.info(f"Update environ: {PYOPENGL_USE_ACCELERATE}={use_accelerate}")

        if self._config.onvif_manager.preload:
            logger.info("Preload ONVIF declarations")
            OnvifManager.preload_onvif_declarations()

        self._onvif_manager = OnvifManager(
            onvif_configs=self._config.onvifs,
            wsdl_config=self._config.wsdl,
            home=self._home,
            update=True,
        )

        self._flow_manager = FlowManager(self._home)
        self._flow_manager.refresh_flow_graphs()
        self._msg_queue = MsgQueue()
        self._supabase = Supabase()

    @property
    def home(self):
        return self._home

    @property
    def config(self):
        return self._config

    @property
    def pm(self):
        return self._process_manager

    @property
    def mq(self):
        return self._msg_queue

    @property
    def fm(self):
        return self._flow_manager

    @property
    def om(self):
        return self._onvif_manager

    @property
    def supabase(self):
        return self._supabase

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

    def make_downloader(self, link: LinkInfo):
        return DownloadArchive.from_link(
            link=link,
            extract_root=self._home,
            cache_dir=self._home.cache,
            temp_dir=self._home.temp,
        )

    def start_download_thread(
        self,
        downloader: DownloadArchive,
        download_timeout: Optional[float] = None,
        verify_checksum=True,
    ):
        return DownloadRunner(
            executor=self._process_manager.thread_pool,
            downloader=downloader,
            download_timeout=download_timeout,
            verify_checksum=verify_checksum,
        )

    def start_flow_thread(self, graph: FlowGraph, start_node: Union[FlowNode, str]):
        runner = FlowRunner(
            executor=self._process_manager.thread_pool,
            graph=graph,
            start_node=start_node,
            use_copy=False,
            use_deepcopy=False,
            debug=self.debug,
            verbose=self.verbose,
        )
        self._flow_manager.runners[graph.key] = runner
        return runner

    def stop_all_flow_runners(self) -> None:
        self._flow_manager.stop_all_runners()

    def teardown_process_manager(self) -> None:
        timeout = self._config.process_manager.teardown_timeout
        self._process_manager.teardown(timeout)

    def save_config(self) -> None:
        self._config.write_yaml(self._home.cvp_yml)
        logger.info(f"Save the config file: '{str(self._home.cvp_yml)}'")

    def save_graph(self, graph: FlowGraph) -> None:
        filepath = self._home.flows.graph_filepath(graph.key)
        self._flow_manager.write_graph_yaml(filepath, graph)
        logger.info(f"Save the graph file: '{str(filepath)}'")

    def save_graphs(self) -> None:
        for graph in self._flow_manager.graphs.values():
            self.save_graph(graph)

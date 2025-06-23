# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.logging.loggers import logger
from cvp.paths.flavour import PathFlavour
from cvp.resources.subdirs.bin import BinPath
from cvp.resources.subdirs.cache import CachePath
from cvp.resources.subdirs.canvases import CanvasesPath
from cvp.resources.subdirs.chat import ChatPath
from cvp.resources.subdirs.downloads import DownloadsPath
from cvp.resources.subdirs.flows import FlowsPath
from cvp.resources.subdirs.jobs import JobsPath
from cvp.resources.subdirs.keyrings import KeyringsPath
from cvp.resources.subdirs.layouts import LayoutsPath
from cvp.resources.subdirs.logs import LogsPath
from cvp.resources.subdirs.mediamtx import MediamtxPath
from cvp.resources.subdirs.medias import MediasPath
from cvp.resources.subdirs.ollamas import OllamasPath
from cvp.resources.subdirs.onvifs import OnvifsPath
from cvp.resources.subdirs.processes import ProcessesPath
from cvp.resources.subdirs.services import ServicesPath
from cvp.resources.subdirs.temp import TempPath
from cvp.resources.subdirs.watchdog import WatchdogPath
from cvp.resources.subdirs.wsdiscovery import WsDiscoveryPath
from cvp.resources.subdirs.wsdl import WsdlPath
from cvp.variables import CVP_YML_FILENAME, GUI_INI_FILENAME, LOGGING_JSON_FILENAME


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

        self.cvp_yml = self.as_path() / CVP_YML_FILENAME
        self.gui_ini = self.as_path() / GUI_INI_FILENAME
        self.logging_json = self.as_path() / LOGGING_JSON_FILENAME

        self.bin = BinPath.classname_subdir(self)
        self.cache = CachePath.classname_subdir(self)
        self.canvases = CanvasesPath.classname_subdir(self)
        self.chat = ChatPath.classname_subdir(self)
        self.downloads = DownloadsPath.classname_subdir(self)
        self.flows = FlowsPath.classname_subdir(self)
        self.jobs = JobsPath.classname_subdir(self)
        self.keyrings = KeyringsPath.classname_subdir(self)
        self.layouts = LayoutsPath.classname_subdir(self)
        self.logs = LogsPath.classname_subdir(self)
        self.ollamas = OllamasPath.classname_subdir(self)
        self.mediamtx = MediamtxPath.classname_subdir(self)
        self.medias = MediasPath.classname_subdir(self)
        self.onvifs = OnvifsPath.classname_subdir(self)
        self.processes = ProcessesPath.classname_subdir(self)
        self.services = ServicesPath.classname_subdir(self)
        self.temp = TempPath.classname_subdir(self)
        self.watchdog = WatchdogPath.classname_subdir(self)
        self.wsdiscovery = WsDiscoveryPath.classname_subdir(self)
        self.wsdl = WsdlPath.classname_subdir(self)

        self._dirs = [
            self.bin,
            self.cache,
            self.canvases,
            self.chat,
            self.downloads,
            self.flows,
            self.jobs,
            self.keyrings,
            self.layouts,
            self.logs,
            self.ollamas,
            self.mediamtx,
            self.medias,
            self.onvifs,
            self.processes,
            self.services,
            self.temp,
            self.watchdog,
            self.wsdiscovery,
            self.wsdl,
        ]

        if not self.exists():
            logger.info(f"Create home directory: '{str(self)}'")
            self.mkdir(parents=True, exist_ok=True)

        for dir_path in self._dirs:
            if not dir_path.exists():
                logger.info(f"Create subdirectory: '{str(dir_path)}'")
                dir_path.mkdir(parents=False, exist_ok=True)

        logger.info("Copy the WSDL files in the package assets")
        self.wsdl.copy_asset_files()

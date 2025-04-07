# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.logging.logging import logger
from cvp.resources.subdirs.bin import Bin
from cvp.resources.subdirs.cache import Cache
from cvp.resources.subdirs.chat import Chat
from cvp.resources.subdirs.flows import Flows
from cvp.resources.subdirs.keyrings import Keyrings
from cvp.resources.subdirs.layouts import Layouts
from cvp.resources.subdirs.logs import Logs
from cvp.resources.subdirs.ollamas import Ollamas
from cvp.resources.subdirs.onvifs import Onvifs
from cvp.resources.subdirs.processes import Processes
from cvp.resources.subdirs.temp import Temp
from cvp.resources.subdirs.wsdl import Wsdl
from cvp.system.path import PathFlavour
from cvp.variables import CVP_YML_FILENAME, GUI_INI_FILENAME, LOGGING_JSON_FILENAME


class HomeDir(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

        self.cvp_yml = self.as_path() / CVP_YML_FILENAME
        self.gui_ini = self.as_path() / GUI_INI_FILENAME
        self.logging_json = self.as_path() / LOGGING_JSON_FILENAME

        self.bin = Bin.classname_subdir(self)
        self.cache = Cache.classname_subdir(self)
        self.chat = Chat.classname_subdir(self)
        self.flows = Flows.classname_subdir(self)
        self.keyrings = Keyrings.classname_subdir(self)
        self.layouts = Layouts.classname_subdir(self)
        self.logs = Logs.classname_subdir(self)
        self.ollamas = Ollamas.classname_subdir(self)
        self.onvifs = Onvifs.classname_subdir(self)
        self.processes = Processes.classname_subdir(self)
        self.temp = Temp.classname_subdir(self)
        self.wsdl = Wsdl.classname_subdir(self)

        self._dirs = [
            self.bin,
            self.cache,
            self.chat,
            self.flows,
            self.keyrings,
            self.layouts,
            self.logs,
            self.ollamas,
            self.onvifs,
            self.processes,
            self.temp,
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

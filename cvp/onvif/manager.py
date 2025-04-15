# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import List

from cvp.config.sections.onvif import OnvifConfig
from cvp.keyring.root import RootKeyring
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.client import OnvifClient
from cvp.onvif.declarations import ONVIF_DECLARATIONS
from cvp.resources.home import HomeDir


class OnvifManager(OrderedDict[str, OnvifClient]):
    def __init__(
        self,
        onvif_configs: List[OnvifConfig],
        home: HomeDir,
        keyring: RootKeyring,
        *,
        update=False,
    ):
        super().__init__()
        self._onvif_configs = onvif_configs
        self._home = home
        self._keyring = keyring

        if onvif_configs and update:
            for onvif_config in onvif_configs:
                self.create_onvif_service(onvif_config, append=True)

    def create_onvif_service(self, onvif_config: OnvifConfig, *, append=False):
        service = OnvifClient(onvif_config, self._home, self._keyring)
        if append:
            self.__setitem__(onvif_config.uuid, service)
        return service

    def get_synced_client(self, onvif_config: OnvifConfig) -> OnvifClient:
        if self.__contains__(onvif_config.uuid):
            service = self.__getitem__(onvif_config.uuid)
            if service.onvif_config == onvif_config:
                return service
            else:
                self.__delitem__(onvif_config.uuid)
        return self.create_onvif_service(onvif_config, append=True)

    @staticmethod
    def preload_onvif_declarations() -> None:
        for i, decl in enumerate(ONVIF_DECLARATIONS):
            prefix = f"[{i + 1}/{len(ONVIF_DECLARATIONS)}]"
            binding = decl.namespace_binding
            try:
                logger.debug(f"{prefix} Load ONVIF wsdl declaration: {binding}")
                decl.load_document()

                logger.debug(f"{prefix} Load ONVIF schema declaration: {binding}")
                decl.load_schema()
            except BaseException as e:
                logger.error(e)

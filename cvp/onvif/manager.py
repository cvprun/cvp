# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Optional, Tuple
from uuid import uuid4

from cvp.keyring.root import RootKeyring
from cvp.onvif.client import OnvifClient
from cvp.onvif.onvif import OnvifConfig
from cvp.resources.home import HomeDir
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.onvifs import OnvifsPath
from cvp.variables import ONVIF_ADDRESS, ONVIF_NONAME


class OnvifManager(ResourceManager[OnvifConfig]):
    def __init__(self, path: OnvifsPath, *, reload=False, raise_errors=False):
        super().__init__(
            cls=OnvifConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        name=ONVIF_NONAME,
        address=ONVIF_ADDRESS,
        *,
        key: Optional[str] = None,
    ) -> Tuple[str, OnvifConfig]:
        key = key if key else str(uuid4())
        config = OnvifConfig(uuid=key, name=name, address=address)
        self.add(key, config)
        return key, config


# class OnvifManager(OrderedDict[str, OnvifClient]):
#     def __init__(
#         self,
#         onvif_configs: List[OnvifConfig],
#         home: HomeDir,
#         keyring: RootKeyring,
#         *,
#         update=False,
#     ):
#         super().__init__()
#         self._onvif_configs = onvif_configs
#         self._home = home
#         self._keyring = keyring
#
#         if onvif_configs and update:
#             for onvif_config in onvif_configs:
#                 self.create_onvif_service(onvif_config, append=True)
#
#     def create_onvif_service(self, onvif_config: OnvifConfig, *, append=False):
#         service = OnvifClient(onvif_config, self._home, self._keyring)
#         if append:
#             self.__setitem__(onvif_config.uuid, service)
#         return service
#
#     def get_synced_client(self, onvif_config: OnvifConfig) -> OnvifClient:
#         if self.__contains__(onvif_config.uuid):
#             service = self.__getitem__(onvif_config.uuid)
#             if service.onvif_config == onvif_config:
#                 return service
#             else:
#                 self.__delitem__(onvif_config.uuid)
#         return self.create_onvif_service(onvif_config, append=True)

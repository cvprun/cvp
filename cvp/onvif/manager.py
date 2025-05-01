# -*- coding: utf-8 -*-

from typing import Dict, Optional, Tuple
from uuid import uuid4

from cvp.onvif.client import OnvifClient
from cvp.onvif.config import OnvifConfig, OnvifKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.onvifs import OnvifsPath
from cvp.variables import ONVIF_ADDRESS, ONVIF_NONAME


class OnvifManager(ResourceManager[OnvifKey, OnvifConfig]):
    _clients: Dict[OnvifKey, OnvifClient]

    def __init__(self, path: OnvifsPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=OnvifKey,
            config_type=OnvifConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._clients = dict()

    def has_client(self, key: OnvifKey) -> bool:
        return key in self._clients

    def add_client(self, key: OnvifKey, client: OnvifClient) -> None:
        self._clients[key] = client

    def get_client(self, key: OnvifKey) -> Optional[OnvifClient]:
        return self._clients.get(key)

    def pop_client(self, key: OnvifKey) -> OnvifClient:
        return self._clients.pop(key)

    def add_config(
        self,
        name=ONVIF_NONAME,
        address=ONVIF_ADDRESS,
        *,
        key: Optional[OnvifKey] = None,
    ) -> Tuple[OnvifKey, OnvifConfig]:
        key = key if key else OnvifKey(str(uuid4()))
        assert key

        config = OnvifConfig(key=key, name=name, address=address)
        self.add(key, config)
        return key, config

# -*- coding: utf-8 -*-

from typing import Dict, Optional, Tuple
from uuid import uuid4

from cvp.onvif.client import OnvifClient
from cvp.onvif.config import OnvifConfig
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.onvifs import OnvifsPath
from cvp.variables import ONVIF_ADDRESS, ONVIF_NONAME


class OnvifManager(ResourceManager[OnvifConfig]):
    _clients: Dict[str, OnvifClient]

    def __init__(self, path: OnvifsPath, *, reload=False, raise_errors=False):
        super().__init__(
            cls=OnvifConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._clients = dict()

    def has_client(self, uuid: str) -> bool:
        return uuid in self._clients

    def add_client(self, uuid: str, client: OnvifClient) -> None:
        self._clients[uuid] = client

    def get_client(self, uuid: str) -> Optional[OnvifClient]:
        return self._clients.get(uuid)

    def pop_client(self, uuid: str) -> OnvifClient:
        return self._clients.pop(uuid)

    def add_config(
        self,
        name=ONVIF_NONAME,
        address=ONVIF_ADDRESS,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[str, OnvifConfig]:
        uuid = uuid if uuid else str(uuid4())
        config = OnvifConfig(uuid=uuid, name=name, address=address)
        self.add(uuid, config)
        return uuid, config

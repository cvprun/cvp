# -*- coding: utf-8 -*-

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.wsdiscovery import WsDiscoveryPath
from cvp.wsdiscovery.wsd import EprKey, WsDiscovery


class WsDiscoveryManager(ResourceManager[EprKey, WsDiscovery]):
    def __init__(self, path: WsDiscoveryPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=EprKey,
            config_type=WsDiscovery,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

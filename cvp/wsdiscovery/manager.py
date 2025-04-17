# -*- coding: utf-8 -*-

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.wsdiscovery import WsDiscoveryPath
from cvp.wsdiscovery.wsd import WsDiscovery


class WsDiscoveryManager(ResourceManager[WsDiscovery]):
    def __init__(self, path: WsDiscoveryPath, *, reload=False, raise_errors=False):
        super().__init__(
            cls=WsDiscovery,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

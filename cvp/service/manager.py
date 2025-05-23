# -*- coding: utf-8 -*-

from typing import Iterable, Optional, Tuple
from uuid import uuid4

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.services import ServicesPath
from cvp.service.item import ServiceItem, ServiceKey


class ServiceManager(ResourceManager[ServiceKey, ServiceItem]):
    def __init__(
        self,
        path: ServicesPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=ServiceKey,
            config_type=ServiceItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_service(
        self,
        args: Optional[Iterable[str]] = None,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[ServiceKey, ServiceItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = ServiceItem(uuid=uuid, args=list(args or ()))
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

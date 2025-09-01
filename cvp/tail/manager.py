# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.tails import TailsPath
from cvp.tail.item import TailItem, TailKey


class TailManager(ResourceManager[TailKey, TailItem]):
    def __init__(
        self,
        path: TailsPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=TailKey,
            config_type=TailItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[TailKey, TailItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = TailItem(uuid=uuid)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

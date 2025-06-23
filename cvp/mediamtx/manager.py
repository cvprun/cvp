# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.mediamtx.item import MediamtxItem, MediamtxKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.mediamtx import MediamtxPath
from cvp.variables import MEDIAMTX_NONAME


class MediamtxManager(ResourceManager[MediamtxKey, MediamtxItem]):
    def __init__(self, path: MediamtxPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=MediamtxKey,
            config_type=MediamtxItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_client(
        self,
        name=MEDIAMTX_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[MediamtxKey, MediamtxItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = MediamtxItem(uuid=uuid, name=name)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

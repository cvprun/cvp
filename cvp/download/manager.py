# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

from cvp.download.item import DownloadItem, DownloadKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.downloads import DownloadsPath


class DownloadManager(ResourceManager[DownloadKey, DownloadItem]):
    def __init__(
        self,
        path: DownloadsPath,
        tmpdir: Path,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=DownloadKey,
            config_type=DownloadItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._tmpdir = tmpdir

    def add_download(
        self,
        url: str,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[DownloadKey, DownloadItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = DownloadItem(uuid=uuid, url=url)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

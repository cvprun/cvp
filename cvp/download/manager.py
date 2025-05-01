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
        key: Optional[DownloadKey] = None,
    ) -> Tuple[DownloadKey, DownloadItem]:
        key = key if key else DownloadKey(str(uuid4()))
        assert key

        item = DownloadItem(key=key, url=url)
        self.add(key, item)
        return key, item

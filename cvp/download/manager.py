# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

from cvp.download.item import DownloadItem
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.downloads import DownloadsPath


class DownloadManager(ResourceManager[DownloadItem]):
    def __init__(
        self,
        path: DownloadsPath,
        tmpdir: Path,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            cls=DownloadItem,
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
    ) -> Tuple[str, DownloadItem]:
        uuid = uuid if uuid else str(uuid4())
        item = DownloadItem(uuid=uuid, url=url)
        self.add(uuid, item)
        return uuid, item

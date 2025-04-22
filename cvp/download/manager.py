# -*- coding: utf-8 -*-

from pathlib import Path

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

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import timedelta

import platformdirs

from cvp.hashfunc.mapping import HashFunction


@dataclass
class DownloaderConfig:
    use_platform_download_dir: bool = True
    download_dir: str = field(default_factory=platformdirs.user_downloads_dir)

    use_timeout = False
    timeout: float = field(default_factory=lambda: timedelta(hours=1).total_seconds())

    checksum: str = field(default_factory=lambda: str(HashFunction.md5))

    follow_redirects: bool = True
    verify_ssl: bool = True

    def update_defaults(self) -> None:
        self.use_platform_download_dir = True
        self.download_dir = platformdirs.user_downloads_dir()
        self.use_timeout = False
        self.timeout = timedelta(hours=1).total_seconds()
        self.checksum = str(HashFunction.md5)
        self.follow_redirects = True
        self.verify_ssl = True

    @property
    def checksum_hash(self) -> HashFunction:
        try:
            return HashFunction(self.checksum)
        except ValueError:
            return HashFunction.md5

    @checksum_hash.setter
    def checksum_hash(self, value: HashFunction) -> None:
        self.checksum = HashFunction(value)

# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from sys import audit
from typing import Any, Final, NamedTuple, Optional, Union
from urllib.parse import urlparse

from zeep.cache import Base as ZeepCacheBase

from cvp.logging.loggers import wsdl_logger as logger
from cvp.types.override import override

CACHE_SET_AUDIT_EVENT: Final[str] = "cvp.wsdl.cache.set"
CACHE_GET_AUDIT_EVENT: Final[str] = "cvp.wsdl.cache.set"


class CacheSetAuditArgs(NamedTuple):
    url: str
    path: PathLike[str]
    error: Optional[BaseException]


class CacheGetAuditArgs(NamedTuple):
    url: str
    data: Optional[bytes]
    error: Optional[BaseException]


class ZeepFileCache(ZeepCacheBase):
    def __init__(self, prefix: Union[str, PathLike[str]], *, readonly=False):
        super().__init__()
        self._prefix = prefix
        self._readonly = readonly

    def get_cache_path(self, url: str) -> Path:
        o = urlparse(url)
        hostname = o.hostname if o.hostname else "__unknown_host__"
        return Path(os.path.join(self._prefix, hostname, *o.path.split("/")))

    @override
    def add(self, url: str, content: Any):
        if self._readonly:
            raise ValueError("Cannot add files to read-only storage")

        filepath = self.get_cache_path(url)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not filepath.exists():
                with filepath.open("wb") as f:
                    f.write(content)
        except BaseException as e:  # noqa
            logger.error(f"{type(self).__name__}.add(url={url}) error: {e}")
            audit(CACHE_SET_AUDIT_EVENT, *CacheSetAuditArgs(url, filepath, e))
        else:
            logger.debug(f"{type(self).__name__}.add(url={url}) ok")
            audit(CACHE_SET_AUDIT_EVENT, *CacheSetAuditArgs(url, filepath, None))

    @override
    def get(self, url: str):
        filepath = self.get_cache_path(url)
        try:
            if filepath.is_file():
                with filepath.open("rb") as f:
                    result = f.read()
        except BaseException as e:  # noqa
            logger.warning(f"{type(self).__name__}.get(url={url}) error: {e}")
            audit(CACHE_GET_AUDIT_EVENT, *CacheGetAuditArgs(url, None, e))
            return None
        else:
            logger.debug(f"{type(self).__name__}.get(url={url}) ok")
            audit(CACHE_GET_AUDIT_EVENT, *CacheGetAuditArgs(url, result, None))
            return result

    @classmethod
    def with_package_asset(cls):
        from cvp.assets.wsdl import get_wsdl_dir

        return cls(get_wsdl_dir(), readonly=True)

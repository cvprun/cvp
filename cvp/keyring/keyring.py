# -*- coding: utf-8 -*-

from os import PathLike
from typing import Dict, NamedTuple, Optional, Union, overload

from cvp.keyring.details import (
    delete_password,
    get_password,
    set_all_filepath,
    set_password,
)
from cvp.variables import KEYRING_EXTENSION


class CacheKey(NamedTuple):
    service: str
    key: str


class Keyring:
    _cache: Dict[CacheKey, str]

    def __init__(self):
        self._cache = dict()

    @staticmethod
    def update_default_filepath(
        path: Union[str, PathLike[str]],
        extension=KEYRING_EXTENSION,
    ) -> None:
        set_all_filepath(path, extension=extension)

    @staticmethod
    def gen_cache_key(service: str, key: str):
        return CacheKey(service, key)

    # fmt: off
    @overload
    def get_password(self, service: str, key: str) -> Optional[str]: ...
    @overload
    def get_password(self, service: str, key: str, default: str) -> str: ...
    # fmt: on

    def get_password(
        self,
        service: str,
        key: str,
        default: Optional[str] = None,
    ) -> Optional[str]:
        cache_key = self.gen_cache_key(service, key)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = get_password(service, key)
        if result is None:
            return default

        self._cache[cache_key] = result
        return result

    # fmt: off
    @overload
    def password(self, service: str, key: str) -> str: ...
    @overload
    def password(self, service: str, key: str, default: str) -> str: ...
    # fmt: on

    def password(
        self,
        service: str,
        key: str,
        default: Optional[str] = None,
    ) -> str:
        return self.get_password(service, key, default if default else str())

    def set_password(self, service: str, key: str, value: str) -> None:
        cache_key = self.gen_cache_key(service, key)
        set_password(service, key, value)
        self._cache[cache_key] = value

    def delete_password(self, service: str, key: str) -> None:
        cache_key = self.gen_cache_key(service, key)
        if cache_key in self._cache:
            self._cache.pop(cache_key)
        if get_password(service, key) is not None:
            delete_password(service, key)

# -*- coding: utf-8 -*-

from enum import StrEnum, unique
from os import PathLike
from typing import Dict, NamedTuple, Optional, Union, overload
from weakref import ReferenceType, ref

from cvp.keyring import details
from cvp.patterns.singleton import singleton
from cvp.variables import KEYRING_EXTENSION


@unique
class KeyringBackendName(StrEnum):
    chainer = details.KEYRING_CHAINER
    encrypted = details.KEYRING_ENCRYPTED
    fail = details.KEYRING_FAIL
    kwallet = details.KEYRING_KWALLET
    macos = details.KEYRING_MACOS
    null = details.KEYRING_NULL
    plain_text = details.KEYRING_PLAIN_TEXT
    sagecipher = details.KEYRING_SAGECIPHER
    secret_service = details.KEYRING_SECRET_SERVICE
    windows = details.KEYRING_WINDOWS


class ServiceKey(NamedTuple):
    service: str
    key: str


@singleton
class RootKeyring:
    _cache: Dict[ServiceKey, str]

    def __init__(self):
        self._cache = dict()

    def clear_cache(self) -> None:
        self._cache.clear()

    @staticmethod
    def update_default_filepath(
        path: Union[str, PathLike[str]],
        extension=KEYRING_EXTENSION,
    ) -> None:
        details.set_all_filepath(path, extension=extension)

    @staticmethod
    def gen_cache_key(service: str, key: str):
        return ServiceKey(service, key)

    @staticmethod
    def is_valid_sagecipher() -> bool:
        return details.is_valid_sagecipher()

    @staticmethod
    def get_backend_name():
        return details.get_keyring().name

    def set_backend_with_name(self, name: KeyringBackendName) -> None:
        backend = details.load_keyring(name)
        details.set_keyring(backend)
        self.clear_cache()

    def has(self, service: str, key: str) -> bool:
        cache_key = self.gen_cache_key(service, key)
        if cache_key in self._cache:
            return True
        return details.get_password(service, key) is not None

    # fmt: off
    @overload
    def get(self, service: str, key: str) -> Optional[str]: ...
    @overload
    def get(self, service: str, key: str, default: str) -> str: ...
    # fmt: on

    def get(
        self,
        service: str,
        key: str,
        default: Optional[str] = None,
    ) -> Optional[str]:
        cache_key = self.gen_cache_key(service, key)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = details.get_password(service, key)
        if result is None:
            return default

        self._cache[cache_key] = result
        return result

    def set(self, service: str, key: str, value: str) -> None:
        cache_key = self.gen_cache_key(service, key)
        details.set_password(service, key, value)
        self._cache[cache_key] = value

    def remove(self, service: str, key: str) -> None:
        cache_key = self.gen_cache_key(service, key)
        if cache_key in self._cache:
            self._cache.pop(cache_key)
        if details.get_password(service, key) is not None:
            details.delete_password(service, key)

    def __contains__(self, item: ServiceKey) -> bool:
        return self.has(item.service, item.key)

    def __getitem__(self, item: ServiceKey) -> Optional[str]:
        return self.get(item.service, item.key)

    def __setitem__(self, item: ServiceKey, value: str) -> None:
        self.set(item.service, item.key, value)

    def __delitem__(self, item: ServiceKey) -> None:
        self.remove(item.service, item.key)

    def get_service(self, service: str):
        return RootKeyringService(self, service)


class RootKeyringService:
    _parent: ReferenceType[RootKeyring]
    _service: str

    def __init__(self, parent: RootKeyring, service: str):
        self._parent = ref(parent)
        self._service = service

    @property
    def parent(self) -> RootKeyring:
        result = self._parent()
        if result is None:
            raise ReferenceError("Expired Keyring object")
        return result

    def has(self, key: str) -> bool:
        return self.parent.has(self._service, key)

    def get(self, key: str) -> Optional[str]:
        return self.parent.get(self._service, key)

    def set(self, key: str, value: str) -> None:
        self.parent.set(self._service, key, value)

    def remove(self, key: str) -> None:
        self.parent.remove(self._service, key)

    def __contains__(self, key: str) -> bool:
        return self.has(key)

    def __getitem__(self, key: str) -> Optional[str]:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove(key)

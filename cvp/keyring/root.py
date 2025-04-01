# -*- coding: utf-8 -*-

from os import PathLike
from typing import Dict, Generic, Optional, TypeVar, Union, overload
from weakref import ReferenceType, ref

from cvp.keyring import details
from cvp.keyring.keys import KeyringBackendName, ServiceKey, ServiceName, SupabaseKey
from cvp.patterns.singleton import singleton
from cvp.variables import KEYRING_EXTENSION


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

    def get_or_empty(self, service: str, key: str) -> str:
        return self.get(service, key, str())

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

    def get_service(self, service: Union[ServiceName, str]):
        if isinstance(service, ServiceName):
            service = str(service)
        assert isinstance(service, str)
        return RootKeyringService[str](self, service)

    @property
    def onvif(self):
        return self.get_service(ServiceName.onvif)

    @property
    def supabase(self):
        return RootKeyringService[SupabaseKey](self, ServiceName.supabase)


_ServiceKeyT = TypeVar("_ServiceKeyT", bound=str)


class RootKeyringService(Generic[_ServiceKeyT]):
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

    def has(self, key: _ServiceKeyT) -> bool:
        return self.parent.has(self._service, key)

    def get(self, key: _ServiceKeyT) -> Optional[str]:
        return self.parent.get(self._service, key)

    def get_or_empty(self, key: _ServiceKeyT) -> str:
        return self.parent.get_or_empty(self._service, key)

    def set(self, key: _ServiceKeyT, value: str) -> None:
        self.parent.set(self._service, key, value)

    def remove(self, key: _ServiceKeyT) -> None:
        self.parent.remove(self._service, key)

    def __contains__(self, key: _ServiceKeyT) -> bool:
        return self.has(key)

    def __getitem__(self, key: _ServiceKeyT) -> Optional[str]:
        return self.get(key)

    def __setitem__(self, key: _ServiceKeyT, value: str) -> None:
        self.set(key, value)

    def __delitem__(self, key: _ServiceKeyT) -> None:
        self.remove(key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

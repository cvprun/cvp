# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from os import PathLike
from typing import Dict, Optional, Tuple, Union

from cvp.keyring.details import (
    delete_password,
    get_password,
    set_all_filepath,
    set_password,
)
from cvp.system.path import PathFlavour
from cvp.variables import KEYRING_EXTENSION


@unique
class ServiceName(StrEnum):
    onvif_password = auto()
    server = auto()


class Keyrings(PathFlavour):
    _password_cache: Dict[Tuple[str, str], str]

    def __init__(self, path: Union[str, PathLike[str]], extension=KEYRING_EXTENSION):
        super().__init__(path)
        self._onvif_password_service_name = ServiceName.onvif_password
        self._server_service_name = ServiceName.server
        self._server_password_key = "password"
        self._server_supabase_key = "supabase_key"
        self._password_cache = dict()
        self._extension = extension

    def update_default_filepath(self) -> None:
        set_all_filepath(self, extension=self._extension)

    def get_password(self, service: str, key: str, default=None) -> Optional[str]:
        cache_key = service, key
        if cache_key in self._password_cache:
            return self._password_cache[cache_key]

        result = get_password(service, key)
        if result is None:
            return default

        self._password_cache[cache_key] = result
        return result

    def set_password(self, service: str, key: str, value: str) -> None:
        cache_key = service, key
        set_password(service, key, value)
        self._password_cache[cache_key] = value

    def delete_password(self, service: str, key: str) -> None:
        cache_key = service, key
        if cache_key in self._password_cache:
            self._password_cache.pop(cache_key)
        if get_password(service, key) is not None:
            delete_password(service, key)

    def get_onvif_password(self, key: str, default=None) -> Optional[str]:
        return self.get_password(self._onvif_password_service_name, key, default)

    def set_onvif_password(self, key: str, value: str) -> None:
        self.set_password(self._onvif_password_service_name, key, value)

    def delete_onvif_password(self, key: str) -> None:
        self.delete_password(self._onvif_password_service_name, key)

    def get_server_supabase_key(self, default=None) -> Optional[str]:
        return self.get_password(
            self._server_service_name,
            self._server_supabase_key,
            default,
        )

    def set_server_supabase_key(self, value: str) -> None:
        self.set_password(self._server_service_name, self._server_supabase_key, value)

    def delete_server_supabase_key(self) -> None:
        self.delete_password(self._server_service_name, self._server_supabase_key)

    def get_server_password(self, default=None) -> Optional[str]:
        return self.get_password(
            self._server_service_name,
            self._server_password_key,
            default,
        )

    def set_server_password(self, value: str) -> None:
        self.set_password(self._server_service_name, self._server_password_key, value)

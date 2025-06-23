# -*- coding: utf-8 -*-

from functools import lru_cache
from os.path import abspath, dirname
from pathlib import Path
from typing import Optional, TypeVar, Union, overload

from dotenv import dotenv_values

from cvp.network.liveness import ServerLivenessProbe


@lru_cache
def get_project_root_path() -> Path:
    return Path(abspath(dirname(__file__))).parent


@lru_cache
def get_project_root_dotenv_test_path() -> Path:
    return get_project_root_path() / ".env.test"


DefaultT = TypeVar("DefaultT", str, bool, int, float)


# fmt: off
@overload
def get_project_root_dotenv_value(key: str) -> Optional[str]: ...
@overload
def get_project_root_dotenv_value(key: str, default: str) -> str: ...
@overload
def get_project_root_dotenv_value(key: str, default: bool) -> bool: ...
@overload
def get_project_root_dotenv_value(key: str, default: int) -> int: ...
@overload
def get_project_root_dotenv_value(key: str, default: float) -> float: ...
# fmt: on


def get_project_root_dotenv_value(
    key: str,
    default: Optional[DefaultT] = None,
) -> Optional[Union[str, bool, int, float]]:
    values = dotenv_values(get_project_root_dotenv_test_path())
    return values.get(key, default)


class TestServerLivenessProbe(ServerLivenessProbe):
    @classmethod
    def from_dotenv(
        cls,
        address_key: str,
        timeout_key: Optional[str] = None,
    ):
        address = get_project_root_dotenv_value(address_key)
        if address is None:
            return cls()

        if timeout_key:
            timeout = get_project_root_dotenv_value(timeout_key, cls.DEFAULT_TIMEOUT)
        else:
            timeout = cls.DEFAULT_TIMEOUT
        assert isinstance(timeout, float)

        return cls(address, timeout)

    def __bool__(self) -> bool:
        return self.is_alive()

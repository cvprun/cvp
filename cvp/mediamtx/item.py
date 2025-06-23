# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, NewType, Optional, Sequence, Tuple
from uuid import uuid4

from httpx import Timeout
from type_serialize import Serializable

from cvp.mediamtx.client import MediamtxApi
from cvp.types.override import override
from cvp.variables import TIMEOUT_INFINITE

MediamtxKey = NewType("MediamtxKey", str)


class MediamtxItem(Serializable):

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"
        url = auto()
        headers = auto()
        follow_redirects = auto()
        timeout = auto()
        model_names = auto()

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
        follow_redirects=True,
        timeout=TIMEOUT_INFINITE,
        model_names: Optional[Sequence[str]] = None,
        *,
        error: Optional[BaseException] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.url = url if url else str()
        self.headers = list(headers if headers else ())
        self.follow_redirects = follow_redirects
        self.timeout = timeout
        self.model_names = list(model_names if model_names else ())
        self._error = error

    def header_as_dict(self) -> Dict[str, str]:
        return {str(k): str(v) for k, v in self.headers}

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.url == other.url
            and self.headers == other.headers
            and self.follow_redirects == other.follow_redirects
            and self.timeout == other.timeout
            and self.model_names == other.model_names
            and self._error == other._error
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        result.follow_redirects = copy(self.follow_redirects)
        result.timeout = copy(self.timeout)
        result.model_names = copy(self.model_names)
        result._error = copy(self._error)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.url = deepcopy(self.url, memo)
        result.headers = deepcopy(self.headers, memo)
        result.follow_redirects = deepcopy(self.follow_redirects, memo)
        result.timeout = deepcopy(self.timeout, memo)
        result.model_names = deepcopy(self.model_names, memo)
        result._error = deepcopy(self._error, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.uuid): self.uuid,
            str(self._Keys.name_): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.header_as_dict(),
            str(self._Keys.follow_redirects): self.follow_redirects,
            str(self._Keys.timeout): self.timeout,
            str(self._Keys.model_names): self.model_names,
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = str(data.get(self._Keys.uuid, str()))
        self.name = str(data.get(self._Keys.name_, str()))
        self.url = str(data.get(self._Keys.url, str()))

        headers = data.get(self._Keys.headers, dict())
        self.headers = list((str(k), str(v)) for k, v in headers.items())

        self.follow_redirects = bool(data.get(self._Keys.follow_redirects, True))
        self.timeout = float(data.get(self._Keys.timeout, TIMEOUT_INFINITE))
        self.model_names = data.get(self._Keys.model_names, list())

        self._error = None

    @property
    def key(self):
        return MediamtxKey(self.uuid)

    @key.setter
    def key(self, value: MediamtxKey) -> None:
        self.uuid = str(value)

    @property
    def has_error(self) -> bool:
        return self._error is not None

    @property
    def error(self):
        return self._error

    @property
    def client(self):
        return MediamtxApi(
            base_url=self.url,
            headers=self.header_as_dict(),
            timeout=Timeout(self.timeout) if 0 < self.timeout else None,
            follow_redirects=self.follow_redirects,
        )

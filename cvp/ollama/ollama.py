# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Optional, Sequence, Tuple

from type_serialize import Serializable

from cvp.types.override import override
from ollama import Client


class Ollama(Serializable):
    _model_names: List[str]

    @unique
    class _Keys(StrEnum):
        name_ = "name"
        url = auto()
        headers = auto()

    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
    ):
        self.name = name if name else str()
        self.url = url if url else str()
        self.headers = list(headers if headers else ())
        self._model_names = list()

    def header_as_dict(self) -> Dict[str, str]:
        return {str(k): str(v) for k, v in self.headers}

    def header_as_list(self) -> List[List[str]]:
        return [[str(k), str(v)] for k, v in self.headers]

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.name == other.name
            and self.url == other.url
            and self.headers == other.headers
            and self._model_names == other._model_names
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        result._model_names = copy(self._model_names)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = deepcopy(self.name, memo)
        result.url = deepcopy(self.url, memo)
        result.headers = deepcopy(self.headers, memo)
        result._model_names = deepcopy(self._model_names, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.name_): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.header_as_list(),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.name = str(data.get(self._Keys.name_, str()))
        self.url = str(data.get(self._Keys.url, str()))
        self.headers = data.get(self._Keys.headers, list())

        self._model_names = list()

    @property
    def model_names(self):
        return self._model_names

    @model_names.setter
    def model_names(self, value: List[str]):
        self._model_names = value

    @property
    def client(self):
        return Client(
            host=self.url,
            headers=self.header_as_dict(),
            follow_redirects=True,
            timeout=None,
            # auth: AuthTypes | None = None,
            # params: QueryParamTypes | None = None,
            # headers: HeaderTypes | None = None,
            # cookies: CookieTypes | None = None,
            # verify: ssl.SSLContext | str | bool = True,
            # cert: CertTypes | None = None,
            # trust_env: bool = True,
            # http1: bool = True,
            # http2: bool = False,
            # proxy: ProxyTypes | None = None,
            # mounts: None | (typing.Mapping[str, BaseTransport | None]) = None,
            # timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
            # follow_redirects: bool = False,
            # limits: Limits = DEFAULT_LIMITS,
            # max_redirects: int = DEFAULT_MAX_REDIRECTS,
            # event_hooks: None | (typing.Mapping[str, list[EventHook]]) = None,
            # base_url: URL | str = "",
            # transport: BaseTransport | None = None,
            # default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
        )

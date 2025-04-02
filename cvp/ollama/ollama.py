# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Mapping, Optional

from type_serialize import Serializable

from cvp.types.override import override
from ollama import Client


class Ollama(Serializable):
    _model_names: List[str]

    @unique
    class _Keys(StrEnum):
        name = auto()
        url = auto()
        headers = auto()

    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ):
        self.name = name if name else str()
        self.url = url if url else str()

        headers = headers if headers else dict()
        self.headers = dict({str(k): str(v) for k, v in headers.items()})

        self._model_names = list()

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.name == other.name
            and self.url == other.url
            and self.headers == other.headers
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = deepcopy(self.name, memo)
        result.url = deepcopy(self.url, memo)
        result.headers = deepcopy(self.headers, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.name): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.headers,
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.name = str(data.get(self._Keys.name, str()))
        self.url = str(data.get(self._Keys.url, str()))

        headers = data.get(self._Keys.headers, {})
        self.headers = {str(k): str(v) for k, v in headers.items()}

    @property
    def model_names(self):
        return self._model_names

    @model_names.setter
    def model_names(self, value: List[str]):
        self._model_names = value

    @property
    def client(self):
        return Client(host=self.url, **self.headers)

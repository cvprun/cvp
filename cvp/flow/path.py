# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from cvp.flow.datas.prefix import Prefix
from cvp.variables import FLOW_PATH_ENCODING, FLOW_PATH_SEPARATOR


def inference_prefix(path: str) -> Prefix:
    if path:
        prefix = path[0]
        if prefix in Prefix.__members__.values():
            return Prefix(prefix)
    return Prefix.none


class FlowPath:
    def __init__(
        self,
        path: str,
        *,
        separator=FLOW_PATH_SEPARATOR,
        encoding=FLOW_PATH_ENCODING,
    ):
        self._path = path
        self._prefix = inference_prefix(path)
        self._separator = separator
        self._encoding = encoding

    def __repr__(self):
        return (
            f"<{type(self).__name__} @{id(self)}"
            f" path='{self._path}'"
            f" separator='{self._separator}'"
            ">"
        )

    def __bool__(self):
        return bool(self._path)

    def __str__(self):
        return self._path

    def __bytes__(self):
        return self._path.encode(self._encoding)

    def __format__(self, format_spec):
        return self._path

    def __hash__(self):
        return hash(self._path)

    def __eq__(self, other):
        if isinstance(other, FlowPath):
            return self._path == other._path
        elif isinstance(other, str):
            return self._path == other
        else:
            return self._path == str(other)

    @property
    def prefix(self):
        return self._prefix

    @property
    def separator(self):
        return self._separator

    @property
    def encoding(self):
        return self._encoding

    @property
    def has_prefix(self):
        return self._prefix != Prefix.none

    @property
    def is_relative(self):
        if self.has_prefix:
            return self._path.removeprefix(self._prefix).startswith(self._separator)
        else:
            return self._path.startswith(self._separator)

    @property
    def is_absolute(self):
        return not self.is_relative

    def normalize(self):
        path = self._path
        end_index = -len(self._separator)
        while path.endswith(self._separator):
            path = path[:end_index]
        return type(self)(path, separator=self._separator, encoding=self._encoding)

    def join(self, path: Union["FlowPath", str]):
        return type(self)(
            str(self.normalize()) + self._separator + str(path),
            separator=self._separator,
            encoding=self._encoding,
        )

    class SplitResult(NamedTuple):
        module: str
        node: str

    def split(self) -> SplitResult:
        index = self._path.rfind(self._separator)
        if index == -1:
            raise IndexError("The path cannot be split")

        module = self._path[:index]
        node_begin = index + 1
        node = self._path[node_begin:]
        return self.SplitResult(module, node)

    def get_module(self) -> str:
        return self.split().module

    def get_node(self) -> str:
        return self.split().node

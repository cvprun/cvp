# -*- coding: utf-8 -*-

from os import PathLike
from typing import Any, Final, Union

from yaml import dump, full_load

from cvp.resources.formats.base import BaseFormatPath
from cvp.types.override import override
from cvp.yaml.dumpers import DefaultDumper

YAML_ENCODING: Final[str] = "utf-8"


class YamlFormatPath(BaseFormatPath):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path, extension=".yml")
        self._encoding = YAML_ENCODING

    @override
    def dumps(self, data: Any) -> bytes:
        return dump(data, Dumper=DefaultDumper).encode(self._encoding)

    @override
    def loads(self, data: bytes) -> Any:
        return full_load(data)

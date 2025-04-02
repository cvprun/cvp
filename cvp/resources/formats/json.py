# -*- coding: utf-8 -*-

from os import PathLike
from typing import Any, Union

import orjson

from cvp.resources.formats._base import BaseFormatPath
from cvp.types.override import override


class JsonFormatPath(BaseFormatPath):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path, extension=".json")

    @override
    def dumps(self, data: Any) -> bytes:
        return orjson.dumps(data)

    @override
    def loads(self, data: bytes) -> Any:
        return orjson.loads(data)

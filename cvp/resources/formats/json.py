# -*- coding: utf-8 -*-

from os import PathLike
from typing import Any, Final, Union

import orjson

from cvp.resources.formats.base import BaseFormatPath
from cvp.types.override import override

JSON_EXTENSION: Final[str] = ".json"


class JsonFormatPath(BaseFormatPath):
    def __init__(
        self,
        *path: Union[str, PathLike[str]],
        extension=JSON_EXTENSION,
    ):
        super().__init__(*path, extension=extension)

    @override
    def dumps(self, data: Any) -> bytes:
        return orjson.dumps(data)

    @override
    def loads(self, data: bytes) -> Any:
        return orjson.loads(data)

# -*- coding: utf-8 -*-

import pickle
from os import PathLike
from typing import Any, Final, Union

from cvp.resources.formats.base import BaseFormatPath
from cvp.types.override import override

PICKLE_PROTOCOL_VERSION: Final[int] = 5
PICKLE_ENCODING: Final[str] = "ASCII"
PICKLE_EXTENSION: Final[str] = ".pickle"


class PickleFormatPath(BaseFormatPath):
    def __init__(
        self,
        *path: Union[str, PathLike[str]],
        extension=PICKLE_EXTENSION,
        encoding=PICKLE_ENCODING,
        protocol_version=PICKLE_PROTOCOL_VERSION,
    ):
        super().__init__(*path, extension=extension)
        self._encoding = encoding
        self._protocol_version = protocol_version

    @override
    def dumps(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._protocol_version)

    @override
    def loads(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._encoding)

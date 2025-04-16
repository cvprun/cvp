# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.resources.formats.json import JsonFormatPath


class OnvifsPath(JsonFormatPath):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)

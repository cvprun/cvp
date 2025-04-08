# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.resources.formats.yaml import YamlFormatPath


class OllamasPath(YamlFormatPath):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.resources.formats.json import JsonFormatPath
from cvp.resources.formats.yaml import YamlFormatPath
from cvp.strings.is_uuid import is_uuid4


class ModbusPath(YamlFormatPath):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)

    def get_device_root_dir(self, uuid: str) -> JsonFormatPath:
        if not is_uuid4(uuid):
            raise ValueError("The UUID value in Modbus must be valid")

        return JsonFormatPath(self.as_path() / uuid)

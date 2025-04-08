# -*- coding: utf-8 -*-

from os import PathLike, remove
from pathlib import Path
from typing import Union

from imgui_bundle import imgui

from cvp.system.path import PathFlavour


class LayoutsPath(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def key_filepath(self, key: str):
        return Path(self / f"{key}.ini")

    def has_layout(self, key: str) -> bool:
        return self.key_filepath(key).exists()

    def save_layout(self, key: str) -> None:
        imgui.save_ini_settings_to_disk(str(self.key_filepath(key)))

    def load_layout(self, key: str) -> None:
        imgui.load_ini_settings_from_disk(str(self.key_filepath(key)))

    def remove_layout(self, key: str) -> None:
        remove(self.key_filepath(key))

# -*- coding: utf-8 -*-

from typing import Dict, Type, TypeVar

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.resources.formats.base import BaseFormatPath
from cvp.variables import RESOURCE_MANAGER_CONFIG_PREFIX

ConfigT = TypeVar("ConfigT")


class ResourceManager(Dict[str, ConfigT]):
    def __init__(
        self,
        cls: Type[ConfigT],
        root_dir: BaseFormatPath,
        *,
        reload=False,
        raise_errors=False,
        config_prefix=RESOURCE_MANAGER_CONFIG_PREFIX,
    ):
        super().__init__()
        self._class = cls
        self._root_dir = root_dir
        self._config_prefix = config_prefix

        if reload:
            self.read_all_config_files(raise_errors=raise_errors)

    @property
    def root_dir(self):
        return self._root_dir.as_path()

    @property
    def class_name(self) -> str:
        return self._class.__name__

    @property
    def config_prefix(self) -> str:
        return self._config_prefix

    @property
    def extension(self) -> str:
        return self._root_dir.extension

    def make_keypath(self, key: str):
        return self._root_dir.make_object_path(key).as_path()

    def read_serialized_config(self, key: str) -> ConfigT:
        result = deserialize(self._root_dir.read_object(key), self._class)
        logger.info(f"Read from {self.class_name} file completed: '{key}'")
        return result

    def write_serialized_config(self, config: ConfigT, key: str) -> int:
        result = self._root_dir.write_object(serialize(config), key)
        logger.info(f"Write to {self.class_name} file completed: '{key}'")
        return result

    def read_all_config_files(self, *, raise_errors=False) -> None:
        for key in self._root_dir.list_object_filenames():
            try:
                self.__setitem__(key, self.read_serialized_config(key))
            except BaseException as e:
                if raise_errors:
                    raise
                cls = self.class_name
                logger.error(f"Failed to read {cls} file '{key}' - reason: '{e}'")

    def write_all_config_files(self, *, raise_errors=False) -> None:
        for key, config in self.items():
            try:
                self.write_serialized_config(config, key)
            except BaseException as e:
                if raise_errors:
                    raise
                cls = self.class_name
                logger.error(f"Failed to write {cls} file '{key}' - reason: '{e}'")

    def add(self, key: str, config: ConfigT) -> None:
        self.write_serialized_config(config, key)
        self.__setitem__(key, config)

    def exists(self, key: str) -> bool:
        return self.make_keypath(key).is_file()

    def remove_file(self, key: str) -> None:
        self._root_dir.remove_object(key)
        logger.info(f"Removed {self.class_name} file: '{key}'")

    def remove(self, key: str) -> None:
        path = self.make_keypath(key)
        if path.is_file():
            path.unlink()
        self.__delitem__(key)

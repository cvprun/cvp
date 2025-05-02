# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Type, TypeVar

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.resources.formats.base import BaseFormatPath

KeyT = TypeVar("KeyT")
ConfigT = TypeVar("ConfigT")


class ResourceManager(Dict[KeyT, ConfigT]):
    def __init__(
        self,
        key_type: Type[KeyT],
        config_type: Type[ConfigT],
        root_dir: BaseFormatPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__()
        self._key_type = key_type
        self._config_type = config_type
        self._root_dir = root_dir

        if reload:
            self.read_all_config_files(raise_errors=raise_errors)

    @property
    def root_dir(self):
        return self._root_dir.as_path()

    @property
    def class_name(self) -> str:
        return self._config_type.__name__

    @property
    def extension(self) -> str:
        return self._root_dir.extension

    def generate_config_filepath(self, key: KeyT) -> Path:
        return self._root_dir.make_object_path(str(key)).as_path()

    def read_serialized_config_file(self, key: KeyT) -> ConfigT:
        result = deserialize(self._root_dir.read_object(str(key)), self._config_type)
        logger.info(f"Read from {self.class_name} file completed: '{str(key)}'")
        return result

    def write_serialized_config_file(self, key: KeyT, config: ConfigT) -> int:
        result = self._root_dir.write_object(serialize(config), str(key))
        logger.info(f"Write to {self.class_name} file completed: '{str(key)}'")
        return result

    def list_config_filenames(self) -> List[str]:
        return self._root_dir.list_object_filenames()

    def list_config_filekeys(self) -> List[KeyT]:
        result = list()
        for filename in self.list_config_filenames():
            name = filename.removesuffix(self._root_dir.extension)
            result.append(self._key_type(name))  # type: ignore[call-arg]
        return result

    def read_all_config_files(self, *, raise_errors=False) -> None:
        for key in self.list_config_filekeys():
            try:
                self.__setitem__(key, self.read_serialized_config_file(key))
            except BaseException as e:
                if raise_errors:
                    raise
                cls = self.class_name
                logger.exception(f"Failed to read {cls} file '{key}' - reason: '{e}'")

    def write_all_config_files(self, *, raise_errors=False) -> None:
        for key, config in self.items():
            try:
                self.write_serialized_config_file(key, config)
            except BaseException as e:
                if raise_errors:
                    raise
                cls = self.class_name
                logger.error(f"Failed to write {cls} file '{key}' - reason: '{e}'")

    def sync(self, *, raise_errors=False) -> None:
        self.write_all_config_files(raise_errors=raise_errors)
        self.clear()
        self.read_all_config_files(raise_errors=raise_errors)

    def exists_config_file(self, key: KeyT) -> bool:
        return self.generate_config_filepath(key).is_file()

    def add(self, key: KeyT, config: ConfigT) -> None:
        self.write_serialized_config_file(key, config)
        self.__setitem__(key, config)

    def remove(self, key: KeyT) -> None:
        path = self.generate_config_filepath(key)
        if path.is_file():
            path.unlink()
            logger.info(f"Removed {self.class_name} file: '{str(key)}'")
        self.__delitem__(key)

    def remove_all(self) -> None:
        for key in list(self.keys()):
            self.remove(key)

# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from typing import Any, Dict, Type, TypeVar, Optional
from pathlib import Path

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.resources.formats.base import BaseFormatPath
from cvp.variables import RESOURCE_MANAGER_CONFIG_PREFIX

ConfigT = TypeVar("ConfigT")


class ResourceManager:
    _configs: Dict[str, ConfigT]

    def __init__(
        self,
        cls: Type[ConfigT],
        root_dir: BaseFormatPath,
        *,
        reload=False,
        raise_errors=False,
        config_prefix=RESOURCE_MANAGER_CONFIG_PREFIX,
    ):
        self._mapping = dict()
        self._class = cls
        self._root_dir = root_dir
        self._config_prefix = config_prefix

        if reload:
            self.reload_all_config_files(raise_errors=raise_errors)

    @property
    def class_name(self):
        return self._class.__name__

    @property
    def root_dir(self):
        return self._root_dir.as_path()

    @property
    def config_prefix(self):
        return self._config_prefix

    @property
    def extension(self):
        return self._root_dir.extension

    def _read_serialized_config(self, key: str) -> ConfigT:
        result = deserialize(self._root_dir.read_object(key), self._class)
        logger.info(f"Read from {self.class_name} file completed: '{key}'")
        return result

    def _write_serialized_config(self, config: ConfigT, key: str) -> int:
        result = self._root_dir.write_object(serialize(config), key)
        logger.info(f"Write to {self.class_name} file completed: '{key}'")
        return result

    def _read_all_config_files(self, *, raise_errors=False) -> Dict[str, ConfigT]:
        result = dict()
        for key in self._root_dir.list_object_filenames():
            try:
                result[key] = self._read_serialized_config(key)
            except BaseException as e:
                if raise_errors:
                    raise
                logger.error(
                    f"Failed to read {self.class_name} file '{key}'"
                    f" - reason: '{e}'"
                )
        return result

    def reload_all_config_files(self, *, raise_errors=False) -> None:
        self._configs = self._read_all_config_files(raise_errors=raise_errors)

    def write_all_config_files(self, *, raise_errors=False) -> None:
        for key, config in self._configs.items():
            try:
                self._write_serialized_config(config, key)
            except BaseException as e:
                if raise_errors:
                    raise
                logger.error(
                    f"Failed to write {self.class_name} file '{key}'"
                    f" - reason: '{e}'"
                )

    def make_path(self, key: str):
        return Path(self._root_dir.make_object_path(key))

    def _write(self, key: str) -> int:
        config = self.__getitem__(key)
        return self._write_serialized_config(config, key)

    def _read(self, key: str) -> ConfigT:
        config = self._read_serialized_config(key)
        self.__setitem__(key, config)
        return config

    def _remove(self, key: str) -> None:
        self.__delitem__(key)
        self._root_dir.remove_object(key)
        logger.info(f"Removed {self.class_name} file: '{key}'")

    def _exists(self, key: str) -> bool:
        return self._root_dir.make_object_path(key).is_file()

    def _add(self, key: str, config: ConfigT) -> int:
        self.__setitem__(key, config)
        dict().clear()
        return self._write_serialized_config(config, key)

    def clear(self) -> None:
        self._mapping.clear()

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__()

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._mapping = copy(self._mapping)
        result._class = copy(self._class)
        result._root_dir = copy(self._root_dir)
        result._config_prefix = copy(self._config_prefix)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result._mapping = deepcopy(self._mapping, memo)
        result._class = deepcopy(self._class, memo)
        result._root_dir = deepcopy(self._root_dir, memo)
        result._config_prefix = deepcopy(self._config_prefix, memo)
        memo[id(self)] = result
        return result

    def get(self, key: str, default: Optional[ConfigT] = None) -> Optional[ConfigT]:
        if default is not None:
            return self._mapping.get(key, default)
        else:
            return self._mapping.get(key)

    def items(self):
        return self._mapping.items()

    def keys(self):
        return self._mapping.keys()

    def values(self):
        return self._mapping.values()

    def __len__(self):
        return self._mapping.__len__()

    def __contains__(self, key: str):
        return self._mapping.__contains__(key)

    def __getitem__(self, key: str) -> ConfigT:
        return self._mapping.__getitem__(key)

    def __setitem__(self, key: str, value: ConfigT) -> None:
        self._mapping.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self._mapping.__delitem__(key)

    def __iter__(self):
        return self._mapping.__iter__()

    def __reversed__(self):
        return self._mapping.__reversed__()

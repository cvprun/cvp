# -*- coding: utf-8 -*-

from typing import Dict, List, Type, TypeVar

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.resources.formats.base import BaseFormatPath
from cvp.variables import RESOURCE_MANAGER_CONFIG_PREFIX

FilenameT = TypeVar("FilenameT", bound=str, contravariant=True)
ConfigT = TypeVar("ConfigT")


class ResourceManager(Dict[FilenameT, ConfigT]):
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

    def read_serialized_config(self, filename: FilenameT) -> ConfigT:
        result = deserialize(self._root_dir.read_object(filename), self._class)
        logger.info(f"Read from {self.class_name} file completed: '{str(filename)}'")
        return result

    def write_serialized_config(self, config: ConfigT, filename: FilenameT) -> int:
        result = self._root_dir.write_object(serialize(config), filename)
        logger.info(f"Write to {self.class_name} file completed: '{str(filename)}'")
        return result

    def list_config_filenames(self) -> List[str]:
        return self._root_dir.list_object_filenames()

    def read_all_config_files(self, *, raise_errors=False) -> Dict[str, ConfigT]:
        result = dict()
        for filename in self.list_config_filenames():
            try:
                result[filename] = self.read_serialized_config(filename)
            except BaseException as e:
                if raise_errors:
                    raise
                else:
                    logger.error(f"Failed to read {self.class_name} file: '{filename}'")
                    result[filename] = ConfigT(error=e)
        return result

    def reload_all_config_files(self, *, raise_errors=False) -> None:
        try:
            result = self.read_all_config_files(raise_errors=raise_errors)
        except:  # noqa
            raise
        else:
            self.clear()
            self.update(result)

    def write_all_config_files(self, *, raise_errors=False) -> None:
        for filename, config in self.items():
            if config.has_error:
                logger.warning(
                    f"Skip write {self.class_name} file: '{filename}'"
                    f" because has error: {config.error}"
                )
                continue

            try:
                self.write_serialized_config(config, filename)
            except BaseException as e:
                if raise_errors:
                    raise
                else:
                    logger.warning(
                        f"Skip write {self.class_name} file: '{filename}'"
                        f" because has error: {e}"
                    )

    def write(self, filename: FilenameT) -> int:
        ollama = self.__getitem__(filename)
        return self.write_serialized_config(ollama, filename)

    def read(self, filename: FilenameT):
        ollama = self.read_serialized_config(filename)
        self.__setattr__(filename, ollama)
        return ollama

    def remove(self, filename: FilenameT) -> None:
        self.__delitem__(filename)
        self._root_dir.remove_object(filename)
        logger.info(f"Removed ollama config file: '{filename}'")

    def exists(self, filename: FilenameT) -> bool:
        return (self._root_dir / filename).is_file()

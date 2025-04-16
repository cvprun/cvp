# -*- coding: utf-8 -*-

from typing import Dict, List, NewType, Optional, Tuple
from uuid import uuid4

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.ollama.ollama import Ollama
from cvp.resources.subdirs.ollamas import OllamasPath
from cvp.variables import OLLAMA_ADDRESS, OLLAMA_NONAME

OllamaFilename = NewType("OllamaFilename", str)


class OllamaManager(Dict[OllamaFilename, Ollama]):
    def __init__(self, path: OllamasPath, *, reload=False, raise_errors=False):
        super().__init__()
        self._path = path

        if reload:
            self.reload_all_files(raise_errors=raise_errors)

    @property
    def path(self):
        return self._path

    def read_serialized_object(self, filename: OllamaFilename) -> Ollama:
        result = deserialize(self._path.read_object(filename), Ollama)
        logger.info(f"Read from Ollama config file completed: '{filename}'")
        return result

    def write_serialized_object(self, ollama: Ollama, filename: OllamaFilename) -> int:
        result = self._path.write_object(serialize(ollama), filename)
        logger.info(f"Write to Ollama config file completed: '{filename}'")
        return result

    def filenames(self) -> List[OllamaFilename]:
        return [OllamaFilename(x) for x in self._path.list_object_filenames()]

    def read_all_files(self, *, raise_errors=False) -> Dict[OllamaFilename, Ollama]:
        result = dict()
        for filename in self.filenames():
            try:
                result[filename] = self.read_serialized_object(filename)
            except BaseException as e:
                if raise_errors:
                    raise
                else:
                    logger.error(f"Failed to read ollama file: '{filename}'")
                    result[filename] = Ollama(error=e)
        return result

    def write_all_files(self) -> None:
        for filename, ollama in self.items():
            if ollama.has_error:
                logger.warning(
                    f"Skip write ollama file: '{filename}'"
                    f" because has error: {ollama.error}"
                )
                continue

            self.write_serialized_object(ollama, filename)

    def write(self, filename: OllamaFilename) -> int:
        ollama = self.__getitem__(filename)
        return self.write_serialized_object(ollama, filename)

    def read(self, filename: OllamaFilename):
        ollama = self.read_serialized_object(filename)
        self.__setattr__(filename, ollama)
        return ollama

    def remove(self, filename: OllamaFilename) -> None:
        self.__delitem__(filename)
        self._path.remove_object(filename)
        logger.info(f"Removed ollama config file: '{filename}'")

    def exists(self, filename: OllamaFilename) -> bool:
        return (self._path / filename).is_file()

    def reload_all_files(self, *, raise_errors=False) -> None:
        try:
            result = self.read_all_files(raise_errors=raise_errors)
        except:  # noqa
            raise
        else:
            self.clear()
            self.update(result)

    def add_new(
        self,
        filename: Optional[OllamaFilename] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Tuple[OllamaFilename, Ollama]:
        if filename is None:
            filename = OllamaFilename(str(uuid4()) + self._path.extension)
        if name is None:
            name = OLLAMA_NONAME
        if url is None:
            url = OLLAMA_ADDRESS

        result = Ollama(name, url)
        self.__setitem__(filename, result)
        return filename, result

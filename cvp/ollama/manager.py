# -*- coding: utf-8 -*-

from typing import Dict, List, Optional
from uuid import uuid4

from type_serialize import deserialize, serialize

from cvp.ollama.ollama import Ollama
from cvp.resources.home import HomeDir
from cvp.variables import DEFAULT_OLLAMA_ADDRESS, DEFAULT_OLLAMA_NAME


class OllamaManager(Dict[str, Ollama]):
    def __init__(self, home: HomeDir, *, reload=False):
        super().__init__()
        self._path = home.ollamas

        if reload:
            self.reload_all_files()

    def read_serialized_object(self, *subpaths: str) -> Ollama:
        return deserialize(self._path.read_object(*subpaths), Ollama)

    def write_serialized_object(self, ollama: Ollama, *paths: str) -> int:
        return self._path.write_object(serialize(ollama), *paths)

    def filenames(self) -> List[str]:
        return self._path.find_object_filenames()

    def read_all_files(self) -> Dict[str, Ollama]:
        return {name: self.read_serialized_object(name) for name in self.filenames()}

    def write_all_files(self) -> None:
        for filename, ollama in self.items():
            self.write_serialized_object(ollama, filename)

    def reload_all_files(self) -> None:
        self.clear()
        self.update(self.read_all_files())

    def add_new(
        self,
        filename: Optional[str] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
    ):
        filename = filename if filename else (str(uuid4()) + self._path.extension)
        name = name if name is not None else DEFAULT_OLLAMA_NAME
        url = url if url is not None else DEFAULT_OLLAMA_ADDRESS

        assert isinstance(filename, str)
        assert isinstance(name, str)
        assert isinstance(url, str)

        result = Ollama(name, url)
        self.__setitem__(filename, result)
        return filename, result

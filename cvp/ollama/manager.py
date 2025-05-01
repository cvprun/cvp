# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.ollama.ollama import Ollama, OllamaKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.ollamas import OllamasPath
from cvp.variables import OLLAMA_ADDRESS, OLLAMA_NONAME


class OllamaManager(ResourceManager[OllamaKey, Ollama]):
    def __init__(self, path: OllamasPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=OllamaKey,
            config_type=Ollama,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        name=OLLAMA_NONAME,
        url=OLLAMA_ADDRESS,
        *,
        key: Optional[OllamaKey] = None,
    ) -> Tuple[OllamaKey, Ollama]:
        key = key if key else OllamaKey(str(uuid4()))
        assert key

        config = Ollama(key=key, name=name, url=url)
        self.add(key, config)
        return key, config

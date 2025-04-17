# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.ollama.ollama import Ollama
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.ollamas import OllamasPath
from cvp.variables import OLLAMA_ADDRESS, OLLAMA_NONAME


class OllamaManager(ResourceManager[Ollama]):
    def __init__(self, path: OllamasPath, *, reload=False, raise_errors=False):
        super().__init__(
            cls=Ollama,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        name=OLLAMA_NONAME,
        url=OLLAMA_ADDRESS,
        *,
        key: Optional[str] = None,
    ) -> Tuple[str, Ollama]:
        key = key if key else str(uuid4())
        config = Ollama(name, url)
        self.add(key, config)
        return key, config

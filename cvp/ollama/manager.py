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
        uuid: Optional[str] = None,
    ) -> Tuple[str, Ollama]:
        uuid = uuid if uuid else str(uuid4())
        config = Ollama(uuid=uuid, name=name, url=url)
        self.add(uuid, config)
        return uuid, config

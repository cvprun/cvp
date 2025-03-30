# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import DEFAULT_OLLAMA_ADDRESS


@dataclass
class ChatConfig:
    ollama_url: str = DEFAULT_OLLAMA_ADDRESS

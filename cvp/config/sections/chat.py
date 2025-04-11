# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Tuple

from cvp.variables import NOT_FOUND_INDEX


@dataclass
class ChatModel:
    server_name: str = field(default_factory=str)
    server_address: str = field(default_factory=str)
    server_key: str = field(default_factory=str)
    model_name: str = field(default_factory=str)

    @property
    def display_name(self):
        return f"{self.server_name}@{self.model_name}"

    @property
    def model_key(self):
        return self.server_address, self.model_name


@dataclass
class ChatConfig:
    selected_server_key: str = field(default_factory=str)
    selected_model_name: str = field(default_factory=str)
    models: List[ChatModel] = field(default_factory=list)

    def clear_models(self) -> None:
        self.models.clear()

    def append_models(self, server_key: str, server_name: str, model_name: str) -> None:
        self.models.append(ChatModel(server_key, server_name, model_name))

    @property
    def model_names(self) -> List[str]:
        return [model.display_name for model in self.models]

    @property
    def selected(self) -> Tuple[str, str]:
        return self.selected_server_key, self.selected_model_name

    @property
    def selected_index(self) -> int:
        for i, model in enumerate(self.models):
            if model.model_key == self.selected:
                return i
        return NOT_FOUND_INDEX

    @selected_index.setter
    def selected_index(self, value: int) -> None:
        if value < 0 or len(self.models) <= value:
            raise IndexError(f"Index out of range: {value}")
        model = self.models[value]
        self.selected_server_key = model.server_address
        self.selected_model_name = model.model_name

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from cvp.nodes.record import NodeRecord


class NodeInterface(ABC):
    @abstractmethod
    def run(self, record: NodeRecord) -> Any:
        raise NotImplementedError

    @abstractmethod
    def on_render(self, record: NodeRecord) -> None:
        raise NotImplementedError

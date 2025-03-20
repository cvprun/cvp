# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin


class NodeInterface(ABC):
    @abstractmethod
    def run(self, record: NodeRecord) -> Pin:
        raise NotImplementedError

    @abstractmethod
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError

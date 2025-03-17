# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import EmptyNextPin
from cvp.types.override import override


class NodeInterface(ABC):
    @abstractmethod
    def run(self, record: NodeRecord) -> Pin:
        raise NotImplementedError

    @abstractmethod
    def render(self, record: NodeRecord) -> None:
        raise NotImplementedError


class NodeBase(NodeInterface):
    @staticmethod
    def nonext():
        return EmptyNextPin()

    @override
    def run(self, record: NodeRecord) -> Pin:
        return self.nonext()

    @override
    def render(self, record: NodeRecord) -> None:
        pass

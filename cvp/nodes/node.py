# -*- coding: utf-8 -*-

from typing import Any, Dict, NewType, Optional, Sequence

from cvp.nodes.interface import NodeInterface
from cvp.nodes.ntype import Ntype
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import EmptyNextPin
from cvp.types.override import override

NodeName = NewType("NodeName", str)


class Node(NodeInterface):
    def __init__(self, *pins: Pin, ntype: Optional[Ntype] = None):
        self.__pins = pins
        self.__ntype = ntype if ntype is not None else Ntype(type(self))

    @property
    def pins(self) -> Sequence[Pin]:
        return self.__pins

    @property
    def ntype(self) -> Ntype:
        return self.__ntype

    @property
    def type(self):
        return self.__ntype.type

    @property
    def path(self):
        return self.__ntype.path

    @property
    def docs(self):
        return self.__ntype.docs

    @property
    def module_path(self) -> str:
        return self.__ntype.module_path

    @property
    def class_name(self) -> str:
        return self.__ntype.class_name

    @staticmethod
    def nonext():
        return EmptyNextPin()

    @override
    def run(self, record: NodeRecord) -> Pin:
        return self.nonext()

    @override
    def render(self, record: NodeRecord) -> None:
        pass

    def __call__(self, *args, **kwargs) -> Dict[PinName, Any]:
        record = NodeRecord.from_call(*args, **kwargs)
        self.run(record)
        return {pin.name: record.get(pin) for pin in self.__pins if pin.is_data_outputs}

# -*- coding: utf-8 -*-

from typing import NewType, Optional, Sequence

from cvp.nodes.base import NodeBase
from cvp.nodes.ntype import Ntype
from cvp.pins.pin import Pin

NodeName = NewType("NodeName", str)


class Node(NodeBase):
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

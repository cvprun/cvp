# -*- coding: utf-8 -*-

from inspect import signature
from typing import Callable, List, NewType, Sequence, Optional

from cvp.nodes.base import NodeBase
from cvp.nodes.ntype import Ntype
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin, ReturnPin

NodeName = NewType("NodeName", str)


class Node(NodeBase):
    def __init__(self, *pins: Pin, ntype: Optional[Ntype] = None):
        self.__pins = pins
        self.__ntype = ntype if ntype is not None else Ntype.from_node(self)

    @classmethod
    def from_callable(cls, func: Callable):
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        pins: List[Pin] = list()
        pins.append(PrevPin())
        pins.append(NextPin())

        sig = signature(func)
        pins.append(ReturnPin.from_return_annotation(sig.return_annotation))

        for param in sig.parameters.values():
            param_pin = Pin.from_parameter(param)
            pins.append(param_pin)

        return cls(*pins, ntype=Ntype(func))

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

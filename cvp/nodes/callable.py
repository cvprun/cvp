# -*- coding: utf-8 -*-

from inspect import signature
from typing import Any, Callable

from cvp.nodes.node import Node
from cvp.nodes.ntype import Ntype
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.override import override


class CallableNode(Node):
    def __init__(self, func: Callable):
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        self._func = func
        self._signature = signature(self._func)

        parameters = self._signature.parameters
        self._params = [Pin.from_parameter(p) for p in parameters.values()]

        return_annotation = self._signature.return_annotation
        self._return = ReturnPin.from_return_annotation(return_annotation)

        self._prev = PrevPin()
        self._next = NextPin()

        super().__init__(
            self._prev,
            self._next,
            *self._params,
            self._return,
            ntype=Ntype(func),
        )

    @override
    def run(self, record: NodeRecord) -> Pin:
        result = self._func(*record.args, **record.kwargs)
        record.set(self._return, result)
        return self._next

    def __call__(self, *args, **kwargs) -> Any:
        result = super().__call__(*args, **kwargs)
        assert isinstance(result, dict)
        assert 1 == len(result)
        assert self._return.name in result
        return result[self._return.name]

# -*- coding: utf-8 -*-

from sys import exc_info
from typing import Any, Dict, Optional, Tuple, TypedDict

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.glyphs.mdi import PLAY
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataOutputPin
from cvp.pins.flows import FlowOutputPin
from cvp.pins.pin import Pin
from cvp.pins.special import EntrypointPin
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class EntrypointOutput(TypedDict):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


class EntrypointNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._start = FlowOutputPin(
            name="start",
            docs="Entrypoint flow signal",
        )
        self._args = DataOutputPin(
            name="args",
            dtype=dtype_registry.get(list),
            docs="Arguments of list type",
        )
        self._kwargs = DataOutputPin(
            name="kwargs",
            dtype=dtype_registry.get(dict),
            docs="Arguments of dict type",
        )

        super().__init__(
            name="entrypoint",
            path="cvp.entrypoint",
            func=None,
            docs="Indicates the starting point of the graph",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._start, self._args, self._kwargs),
            tags=("entrypoint", "main"),
        )

    @override
    def run(self, pin: Pin, record: NodeRecord) -> Optional[Pin]:
        try:
            if not isinstance(pin, EntrypointPin):
                raise TypeError(
                    "The 'pin' argument must be an instance of"
                    f" {EntrypointPin.__name__}"
                )

            result = EntrypointOutput(args=record.args, kwargs=record.kwargs)
            record.set_result(result)
        except:  # noqa
            record.set_exception(exc_info())

        return self._start

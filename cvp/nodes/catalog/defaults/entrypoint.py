# -*- coding: utf-8 -*-

from sys import exc_info
from typing import Any, Dict, Optional, Tuple, TypedDict

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.glyphs.mdi import PLAY
from cvp.nodes.node import NodeTemplate
from cvp.nodes.pin.datas import DataOutputPinTemplate
from cvp.nodes.pin.flows import FlowOutputPinTemplate
from cvp.nodes.pin.pin import PinTemplate
from cvp.nodes.pin.special import EntrypointPinTemplate
from cvp.nodes.record import FlowRecord
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class EntrypointOutput(TypedDict):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


class EntrypointNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._start = FlowOutputPinTemplate(
            name="start",
            docs="Entrypoint flow signal",
        )
        self._args = DataOutputPinTemplate(
            name="args",
            dtype=dtype_registry.get(list).path,
            docs="Arguments of list type",
        )
        self._kwargs = DataOutputPinTemplate(
            name="kwargs",
            dtype=dtype_registry.get(dict).path,
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
    def run(self, pin: PinTemplate, context: FlowRecord) -> Optional[PinTemplate]:
        try:
            if not isinstance(pin, EntrypointPinTemplate):
                raise TypeError(
                    "The 'pin' argument must be an instance of"
                    f" {EntrypointPinTemplate.__name__}"
                )

            result = EntrypointOutput(args=context.args, kwargs=context.kwargs)
            context.set_result(result)
        except:  # noqa
            context.set_exception(exc_info())

        return self._start

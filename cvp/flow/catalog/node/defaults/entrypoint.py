# -*- coding: utf-8 -*-

from sys import exc_info
from typing import Any, Dict, Optional, Tuple, TypedDict

from cvp.flow.context import FlowContext
from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import PinTemplate
from cvp.flow.templates.pin_datas import DataOutputPinTemplate
from cvp.flow.templates.pin_flows import FlowOutputPinTemplate
from cvp.flow.templates.pin_flows_special import EntrypointPinTemplate
from cvp.fonts.glyphs.mdi import PLAY
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class EntrypointOutput(TypedDict):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


class Entrypoint(NodeTemplate):
    def __init__(self):
        self._flow_start = FlowOutputPinTemplate(name="start")
        self._data_args = DataOutputPinTemplate(name="args")
        self._data_kwargs = DataOutputPinTemplate(name="kwargs")

        super().__init__(
            name="entrypoint",
            path="cvp.entrypoint",
            func=None,
            docs="Indicates the starting point of the graph",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._flow_start, self._data_args, self._data_kwargs),
            tags=("entrypoint", "main"),
        )

    @override
    def run(self, pin: PinTemplate, context: FlowContext) -> Optional[PinTemplate]:
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

        return self._flow_start

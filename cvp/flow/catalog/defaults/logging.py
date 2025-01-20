# -*- coding: utf-8 -*-

from logging import DEBUG
from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.flow.record import FlowRecord
from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import PinTemplate
from cvp.flow.templates.pin.datas import DataInputPinTemplate
from cvp.flow.templates.pin.special import PrevPinTemplate
from cvp.fonts.glyphs.mdi import PLAY
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class LoggingNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPinTemplate()
        self._level = DataInputPinTemplate(
            name="level",
            dtype="builtins.int",
            default=DEBUG,
        )
        self._message = DataInputPinTemplate(name="message", dtype="builtins.str")
        self._logger = DataInputPinTemplate(name="logger", dtype="builtins.str")

        super().__init__(
            name="logging",
            path="cvp.logging",
            func=None,
            docs="Indicates the starting point of the graph",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._prev, self._level, self._message),
            tags=("logging",),
        )

    @override
    def run(self, pin: PinTemplate, context: FlowRecord) -> Optional[PinTemplate]:
        return None

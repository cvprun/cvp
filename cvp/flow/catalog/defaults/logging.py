# -*- coding: utf-8 -*-

from sys import exc_info
from logging import DEBUG, getLogger
from typing import Any, Dict, Optional, TypedDict

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.flow.record import FlowRecord
from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import PinTemplate
from cvp.flow.templates.pin.datas import DataInputPinTemplate
from cvp.flow.templates.pin.special import NextPinTemplate, PrevPinTemplate
from cvp.fonts.glyphs.mdi import PLAY
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override
from cvp.logging.variables import CVP_FLOW_LOGGER_NAME


class LoggingNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPinTemplate()
        self._next = NextPinTemplate()
        self._name = DataInputPinTemplate(
            name="name",
            dtype=dtype_registry.get(str).path,
            docs="Logger's name",
            default=CVP_FLOW_LOGGER_NAME,
        )
        self._level = DataInputPinTemplate(
            name="level",
            dtype=dtype_registry.get(int).path,
            docs="The threshold of this logger",
            default=DEBUG,
        )
        self._msg = DataInputPinTemplate(
            name="msg",
            dtype=dtype_registry.get(str).path,
            docs="The message format string",
            default=str(),
        )

        super().__init__(
            name="logging",
            path="cvp.logging",
            func=None,
            docs="Logs a message with integer level level on this logger",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._prev, self._next, self._name, self._level, self._msg),
            tags=("logging",),
        )

    @override
    def run(self, pin: PinTemplate, context: FlowRecord) -> Optional[PinTemplate]:
        assert pin == self._prev

        try:
            logger_name = context.get(self._name.name)
            logger = getLogger(logger_name)
            logger.log(
                level=context.get(self._level.name),
                msg=context.get(self._msg.name),
            )
            context.set_result(None)
        except:  # noqa
            context.set_exception(exc_info())

        return self._next

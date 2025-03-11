# -*- coding: utf-8 -*-

from logging import DEBUG, getLogger
from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.glyphs.mdi import PLAY
from cvp.logging.variables import CVP_FLOW_LOGGER_NAME
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodePath, NodeTemplate
from cvp.pins.datas import DataInputPinTemplate
from cvp.pins.special import NextPinTemplate, PrevPinTemplate
from cvp.pins.template import PinTemplate
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class LoggingNodeTemplate(NodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPinTemplate()
        self._next = NextPinTemplate()
        self._name = DataInputPinTemplate(
            name="name",
            dtype=dtype_registry.get(str),
            docs="Logger's name",
            default=CVP_FLOW_LOGGER_NAME,
        )
        self._level = DataInputPinTemplate(
            name="level",
            dtype=dtype_registry.get(int),
            docs="The threshold of this logger",
            default=DEBUG,
        )
        self._msg = DataInputPinTemplate(
            name="msg",
            dtype=dtype_registry.get(str),
            docs="The message format string",
            default=str(),
        )

        super().__init__(
            path=NodePath("cvp.essential.logging"),
            name="Logging",
            func=None,
            docs="Logs a message with integer level level on this logger",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._prev, self._next, self._name, self._level, self._msg),
            tags=("logging",),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[PinTemplate]:
        logger_name = record.get(self._name)
        logger = getLogger(logger_name)
        logger.log(level=record.get(self._level), msg=record.get(self._msg))
        return self._next

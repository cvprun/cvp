# -*- coding: utf-8 -*-

from logging import DEBUG, getLogger
from sys import exc_info
from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.glyphs.mdi import PLAY
from cvp.logging.variables import CVP_FLOW_LOGGER_NAME
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class LoggingNode(Node):
    def __init__(self, dtype_registry: DtypeRegistry):
        self._prev = PrevPin()
        self._next = NextPin()
        self._name = DataInputPin(
            name="name",
            dtype=dtype_registry.get(str),
            docs="Logger's name",
            default=CVP_FLOW_LOGGER_NAME,
        )
        self._level = DataInputPin(
            name="level",
            dtype=dtype_registry.get(int),
            docs="The threshold of this logger",
            default=DEBUG,
        )
        self._msg = DataInputPin(
            name="msg",
            dtype=dtype_registry.get(str),
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
    def run(self, pin: Pin, record: NodeRecord) -> Optional[Pin]:
        assert pin == self._prev

        try:
            logger_name = record.get(self._name)
            logger = getLogger(logger_name)
            logger.log(level=record.get(self._level), msg=record.get(self._msg))
            record.result = None
        except:  # noqa
            record.exception = exc_info()

        return self._next

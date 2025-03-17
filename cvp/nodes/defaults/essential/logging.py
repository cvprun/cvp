# -*- coding: utf-8 -*-

from logging import DEBUG, getLogger

from cvp.dtypes.dtype import Dtype
from cvp.logging.variables import CVP_FLOW_LOGGER_NAME
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import NextPin, PrevPin
from cvp.types.override import override


class Logging(Node):
    """Logs a message with integer level on this logger"""

    def __init__(self):
        self._prev = PrevPin()
        self._next = NextPin()
        self._name = DataInputPin(
            name=PinName("name"),
            dtype=Dtype(str),
            docs="Logger's name",
            default=CVP_FLOW_LOGGER_NAME,
        )
        self._level = DataInputPin(
            name=PinName("level"),
            dtype=Dtype(int),
            docs="The threshold of this logger",
            default=DEBUG,
        )
        self._msg = DataInputPin(
            name=PinName("msg"),
            dtype=Dtype(str),
            docs="The message format string",
            default=str(),
        )
        super().__init__(self._prev, self._next, self._name, self._level, self._msg)

    @override
    def run(self, record: NodeRecord) -> Pin:
        logger_name = record.get(self._name)
        logger = getLogger(logger_name)
        logger.log(level=record.get(self._level), msg=record.get(self._msg))
        return self._next

# -*- coding: utf-8 -*-

from logging import Handler, LogRecord
from typing import Callable

from overrides import override


class CallableHandler(Handler):
    def __init__(self, callback: Callable[[LogRecord, str], None]):
        super().__init__()
        self._callback = callback

    @override
    def emit(self, record: LogRecord):
        self._callback(record, self.format(record))

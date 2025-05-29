# -*- coding: utf-8 -*-

from logging import LogRecord
from typing import NamedTuple


class FormattedLogRecord(NamedTuple):
    log: LogRecord
    formatted_message: str

    @classmethod
    def from_log(cls, record: LogRecord, formatted_message: str):
        return cls(record, formatted_message)

    @property
    def args(self):
        return self.log.args

    @property
    def asctime(self):
        return self.log.asctime

    @property
    def created(self):
        return self.log.created

    @property
    def exc_info(self):
        return self.log.exc_info

    @property
    def exc_text(self):
        return self.log.exc_text

    @property
    def filename(self):
        return self.log.filename

    @property
    def func_name(self):
        return self.log.funcName

    @property
    def levelname(self):
        return self.log.levelname

    @property
    def levelno(self):
        return self.log.levelno

    @property
    def lineno(self):
        return self.log.lineno

    @property
    def module(self):
        return self.log.module

    @property
    def msecs(self):
        return self.log.msecs

    @property
    def msg(self):
        return self.log.msg

    @property
    def name(self):
        return self.log.name

    @property
    def pathname(self):
        return self.log.pathname

    @property
    def process(self):
        return self.log.process

    @property
    def process_name(self):
        return self.log.processName

    @property
    def relative_created(self):
        return self.log.relativeCreated

    @property
    def stack_info(self):
        return self.log.stack_info

    @property
    def thread(self):
        return self.log.thread

    @property
    def thread_name(self):
        return self.log.threadName

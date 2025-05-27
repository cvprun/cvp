# -*- coding: utf-8 -*-

from logging import DEBUG, ERROR, INFO, WARNING, Logger
from multiprocessing import get_context
from multiprocessing.queues import Queue
from typing import List, Optional, Union

from cvp.debugging.markers import (
    __MSG_ADD_A_NEW_TODO__,
    __TOAST_FS_EVENTS_PAIR__,
    __WATCHDOG_FS_EVENTS_PAIR__,
)
from cvp.logging.logging import convert_level_number
from cvp.msgs.msg import Msg
from cvp.msgs.msg_type import MsgType, MsgTypeLike
from cvp.process.context import MultiprocessingContextMethod


class MsgQueue(Queue[Msg]):
    def __init__(
        self,
        maxsize=0,
        method: Optional[MultiprocessingContextMethod] = None,
    ):
        super().__init__(maxsize, ctx=get_context(method))

    def pull(self, block=True, timeout: Optional[float] = None) -> List[Msg]:
        result = list()
        while True:
            try:
                result.append(self.get(block, timeout))
            except:  # noqa
                break
        return result

    def pull_nowait(self) -> List[Msg]:
        result = list()
        while True:
            try:
                result.append(self.get_nowait())
            except:  # noqa
                break
        return result

    @staticmethod
    def make_msg(mtype: MsgTypeLike, **kwargs) -> Msg:
        return Msg(mtype=mtype, **kwargs)

    def append_msg(self, mtype: MsgTypeLike, /, **kwargs):
        msg = self.make_msg(mtype, **kwargs)
        assert isinstance(msg.uuid, str)
        assert 1 <= len(msg.uuid)
        self.put(msg, block=True, timeout=None)
        return msg

    assert __TOAST_FS_EVENTS_PAIR__, "Toast methods BEGIN"

    def append_toast(self, message: str, level: Optional[Union[int, str]] = None):
        return self.append_msg(MsgType.toast, message=message, level=level)

    def toast(
        self,
        message: str,
        level: Optional[Union[int, str]] = None,
        logger: Optional[Logger] = None,
    ):
        if logger is not None:
            logger.log(convert_level_number(level), message)
        return self.append_toast(message, level)

    def toast_error(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, ERROR, logger=logger)

    def toast_warning(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, WARNING, logger=logger)

    def toast_info(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, INFO, logger=logger)

    def toast_debug(self, message: str, logger: Optional[Logger] = None):
        return self.toast(message, DEBUG, logger=logger)

    assert __TOAST_FS_EVENTS_PAIR__, "Toast methods END"
    assert __WATCHDOG_FS_EVENTS_PAIR__, "Watchdog filesystem events BEGIN"

    def file_moved(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_moved, src=src, dest=dest, isdir=isdir)

    def file_created(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_created, src=src, dest=dest, isdir=isdir)

    def file_deleted(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_deleted, src=src, dest=dest, isdir=isdir)

    def file_modified(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_modified, src=src, dest=dest, isdir=isdir)

    def file_closed(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_closed, src=src, dest=dest, isdir=isdir)

    def file_closed_no_write(self, src: str, dest: str, isdir: bool):
        return self.append_msg(
            MsgType.file_closed_no_write,
            src=src,
            dest=dest,
            isdir=isdir,
        )

    def file_opened(self, src: str, dest: str, isdir: bool):
        return self.append_msg(MsgType.file_opened, src=src, dest=dest, isdir=isdir)

    assert __WATCHDOG_FS_EVENTS_PAIR__, "Watchdog filesystem events END"
    assert __MSG_ADD_A_NEW_TODO__, "Insert the 'msg' method here."

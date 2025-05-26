# -*- coding: utf-8 -*-

from logging import DEBUG, ERROR, INFO, WARNING, Logger
from typing import Deque, Optional, Union

from cvp.debugging.markers import (
    __MSG_ADD_A_NEW_TODO__,
    __TOAST_FS_EVENTS_PAIR__,
    __WATCHDOG_FS_EVENTS_PAIR__,
)
from cvp.logging.logging import convert_level_number
from cvp.msgs.msg import Msg
from cvp.msgs.msg_type import MsgType, MsgTypeLike


class MsgQueue(Deque[Msg]):
    def get(self):
        result = list()
        while True:
            try:
                result.append(self.popleft())
            except IndexError:
                break
        return result

    @staticmethod
    def make_msg(mtype: MsgTypeLike, **kwargs) -> Msg:
        return Msg(mtype=mtype, **kwargs)

    def append_msg(self, mtype: MsgTypeLike, /, **kwargs):
        msg = self.make_msg(mtype, **kwargs)
        assert isinstance(msg.uuid, str)
        assert 1 <= len(msg.uuid)
        self.append(msg)
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

    def file_moved(self, file: str):
        return self.append_msg(MsgType.file_moved, file=file)

    def file_created(self, file: str):
        return self.append_msg(MsgType.file_created, file=file)

    def file_deleted(self, file: str):
        return self.append_msg(MsgType.file_deleted, file=file)

    def file_modified(self, file: str):
        return self.append_msg(MsgType.file_modified, file=file)

    def file_closed(self, file: str):
        return self.append_msg(MsgType.file_closed, file=file)

    def file_closed_no_write(self, file: str):
        return self.append_msg(MsgType.file_closed_no_write, file=file)

    def file_opened(self, file: str):
        return self.append_msg(MsgType.file_opened, file=file)

    assert __WATCHDOG_FS_EVENTS_PAIR__, "Watchdog filesystem events END"
    assert __MSG_ADD_A_NEW_TODO__, "Insert the 'msg' method here."

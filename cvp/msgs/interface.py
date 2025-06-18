# -*- coding: utf-8 -*-

from abc import ABCMeta
from datetime import datetime
from typing import Optional, Union

from cvp.debugging.markers import (
    __MSG_ADD_A_NEW_TODO__,
    __PROCESS_POLL_EVENTS_PAIR__,
    __SCHEDULER_EVENTS_PAIR__,
    __TOAST_EVENTS_PAIR__,
    __WATCHDOG_EVENTS_PAIR__,
)
from cvp.msgs.abc import abstractmsg
from cvp.msgs.msg_type import MsgType


class MsgInterface(metaclass=ABCMeta):
    @abstractmsg(MsgType.none)
    def on_msg_none(self):
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    assert __TOAST_EVENTS_PAIR__, "Toast methods BEGIN"
    # ----------------------------------------------------------------------------------

    @abstractmsg(MsgType.toast)
    def on_msg_toast(self, message: str, level: Optional[Union[int, str]] = None):
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    assert __TOAST_EVENTS_PAIR__, "Toast methods END"
    assert __WATCHDOG_EVENTS_PAIR__, "Watchdog filesystem events BEGIN"
    # ----------------------------------------------------------------------------------

    @abstractmsg(MsgType.file_moved)
    def on_file_moved(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_created)
    def on_file_created(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_deleted)
    def on_file_deleted(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_modified)
    def on_file_modified(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_closed)
    def on_file_closed(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_closed_no_write)
    def on_file_closed_no_write(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    @abstractmsg(MsgType.file_opened)
    def on_file_opened(self, src: str, dest: str, isdir: bool):
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    assert __WATCHDOG_EVENTS_PAIR__, "Watchdog filesystem events END"
    assert __PROCESS_POLL_EVENTS_PAIR__, "Process polling events BEGIN"
    # ----------------------------------------------------------------------------------

    @abstractmsg(MsgType.process_exited)
    def on_process_exit(self, key: str, pid: int, code: int):
        raise NotImplementedError

    @abstractmsg(MsgType.process_restart)
    def on_process_restart(self, key: str):
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    assert __PROCESS_POLL_EVENTS_PAIR__, "Process polling events END"
    assert __SCHEDULER_EVENTS_PAIR__, "Scheduler events BEGIN"
    # ----------------------------------------------------------------------------------

    @abstractmsg(MsgType.job_scheduled)
    def on_job_scheduled(self, key: str, timestamp: datetime):
        raise NotImplementedError

    @abstractmsg(MsgType.job_completed)
    def on_job_completed(self, key: str):
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    assert __SCHEDULER_EVENTS_PAIR__, "Scheduler events END"
    assert __MSG_ADD_A_NEW_TODO__, "Insert the 'msg' method here."  # TODO
    # ----------------------------------------------------------------------------------

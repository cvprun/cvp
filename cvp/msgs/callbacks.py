# -*- coding: utf-8 -*-

from typing import Optional, Union

from cvp.debugging.markers import (
    __MSG_ADD_A_NEW_TODO__,
    __PROCESS_POLL_EVENTS_PAIR__,
    __TOAST_EVENTS_PAIR__,
    __WATCHDOG_EVENTS_PAIR__,
)
from cvp.msgs.interface import MsgInterface
from cvp.types.override import override


class MsgCallbacks(MsgInterface):
    @override
    def on_msg_none(self):
        pass

    # ----------------------------------------------------------------------------------
    assert __TOAST_EVENTS_PAIR__, "Toast methods BEGIN"
    # ----------------------------------------------------------------------------------

    @override
    def on_msg_toast(self, message: str, level: Optional[Union[int, str]] = None):
        pass

    # ----------------------------------------------------------------------------------
    assert __TOAST_EVENTS_PAIR__, "Toast methods END"
    assert __WATCHDOG_EVENTS_PAIR__, "Watchdog filesystem events BEGIN"
    # ----------------------------------------------------------------------------------

    @override
    def on_file_moved(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_created(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_deleted(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_modified(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_closed(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_closed_no_write(self, src: str, dest: str, isdir: bool):
        pass

    @override
    def on_file_opened(self, src: str, dest: str, isdir: bool):
        pass

    # ----------------------------------------------------------------------------------
    assert __WATCHDOG_EVENTS_PAIR__, "Watchdog filesystem events END"
    assert __PROCESS_POLL_EVENTS_PAIR__, "Process polling events BEGIN"
    # ----------------------------------------------------------------------------------

    @override
    def on_process_exit(self, key: str, pid: int, code: int):
        pass

    # ----------------------------------------------------------------------------------
    assert __PROCESS_POLL_EVENTS_PAIR__, "Process polling events END"
    assert __MSG_ADD_A_NEW_TODO__, "Insert the 'msg' method here."  # TODO
    # ----------------------------------------------------------------------------------

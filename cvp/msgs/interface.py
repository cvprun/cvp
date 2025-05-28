# -*- coding: utf-8 -*-

from abc import ABCMeta
from typing import Optional, Union

from cvp.msgs.abc import abstractmsg
from cvp.msgs.msg_type import MsgType


class MsgInterface(metaclass=ABCMeta):
    @abstractmsg(MsgType.none)
    def on_msg_none(self):
        raise NotImplementedError

    @abstractmsg(MsgType.toast)
    def on_msg_toast(self, message: str, level: Optional[Union[int, str]] = None):
        raise NotImplementedError

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

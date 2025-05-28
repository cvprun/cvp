# -*- coding: utf-8 -*-

from typing import Optional, Union

from cvp.msgs.interface import MsgInterface
from cvp.types.override import override


class MsgCallbacks(MsgInterface):
    @override
    def on_msg_none(self):
        pass

    @override
    def on_msg_toast(self, message: str, level: Optional[Union[int, str]] = None):
        pass

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

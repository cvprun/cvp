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

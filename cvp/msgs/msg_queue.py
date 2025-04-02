# -*- coding: utf-8 -*-

from typing import Deque, Optional, Union

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

    def append_toast(self, message: str, level: Optional[Union[int, str]] = None):
        return self.append_msg(MsgType.toast, message=message, level=level)

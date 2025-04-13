# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin
from cvp.msgs.msg import Msg


class ActivityMixin(BaseContextMixin):
    def do_activity_msg(self, msg: Msg) -> bool:
        assert self
        assert msg
        return False

    def do_activity_process(self) -> None:
        pass

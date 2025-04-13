# -*- coding: utf-8 -*-

from typing import Optional

from cvp.activities._interface import ActivityInterface
from cvp.activities.status import ActivityStatus
from cvp.msgs.msg import Msg
from cvp.types.override import override


class BaseActivity(ActivityInterface):
    @override
    def on_create(self, memo: Msg) -> None:
        pass

    @override
    def on_restart(self) -> None:
        pass

    @override
    def on_start(self) -> None:
        pass

    @override
    def on_resume(self) -> None:
        pass

    # ----------------------------------------------------------------------------------
    # [ activity running ] -------------------------------------------------------------

    @override
    def on_msg(self, msg: Msg) -> Optional[bool]:
        pass

    @override
    def on_before_process(self) -> None:
        pass

    @override
    def on_main_process(self) -> None:
        pass

    @override
    def on_after_process(self) -> None:
        pass

    @override
    def on_next(self) -> Optional[ActivityStatus]:
        pass

    # ----------------------------------------------------------------------------------

    @override
    def on_pause(self) -> None:
        pass

    @override
    def on_stop(self) -> None:
        pass

    @override
    def on_destroy(self) -> None:
        pass

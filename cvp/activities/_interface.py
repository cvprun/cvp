# -*- coding: utf-8 -*-
# https://developer.android.com/guide/components/activities/intro-activities
# https://developer.android.com/reference/android/app/Activity

from abc import ABC, abstractmethod
from typing import Optional

from cvp.activities.status import ActivityStatus
from cvp.msgs.msg import Msg


class ActivityInterface(ABC):
    @abstractmethod
    def on_create(self, memo: Msg) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_restart(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_resume(self) -> None:
        raise NotImplementedError

    # ----------------------------------------------------------------------------------
    # [ activity running ] -------------------------------------------------------------

    @abstractmethod
    def on_msg(self, msg: Msg) -> Optional[bool]:
        raise NotImplementedError

    @abstractmethod
    def on_before_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_main_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_after_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_next(self) -> Optional[ActivityStatus]:
        raise NotImplementedError

    # ----------------------------------------------------------------------------------

    @abstractmethod
    def on_pause(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self) -> None:
        raise NotImplementedError

# -*- coding: utf-8 -*-

from threading import Thread
from typing import Optional
from weakref import ReferenceType, ref

from cvp.msgs.msg_queue import MsgQueue
from cvp.process.process import Process
from cvp.types.override import override


class ServicePollDispatcher(Thread):
    _msgs: ReferenceType[MsgQueue]

    def __init__(
        self,
        msgs: MsgQueue,
        process: Process,
        *,
        name: Optional[str] = None,
        key: Optional[str] = None,
    ):
        super().__init__(name=name or f"<{type(self).__name__} {process.name}>")
        self._msgs = ref(msgs)
        self._process = process
        self._pid = process.pid
        self._key = key if key else str()

    @property
    def msgs(self) -> MsgQueue:
        result = self._msgs()
        if result is None:
            raise ReferenceError("Expired msgs instance")
        return result

    @override
    def run(self) -> None:
        try:
            self._process.wait()
        finally:
            exit_code = self._process.poll()
            assert exit_code is not None
            code = exit_code
            self.msgs.process_exit(self._key, self._pid, code)

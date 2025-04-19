# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.process.process import Process
from cvp.types.override import override


@runtime_checkable
class ProcessTabNameProtocol(Protocol):
    __cvp_process_tab_name__: str


class ProcessTabInterface(ABC):
    @classmethod
    @abstractmethod
    def get_tab_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self, process: Process) -> None:
        raise NotImplementedError


class BaseProcessTab(ProcessTabInterface, ProcessTabNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, ProcessTabNameProtocol)
        self._context = context

    @classmethod
    @override
    def get_tab_name(cls) -> str:
        return cls.__cvp_process_tab_name__

    @property
    def context(self) -> Context:
        return self._context

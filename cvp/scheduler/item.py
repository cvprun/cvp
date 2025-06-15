# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, NewType, Optional
from uuid import uuid4

from cvp.scheduler.predefined import EVERY_MINUTE
from cvp.variables import INFINITE

JobKey = NewType("JobKey", str)


@dataclass
class JobItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    cron: str = EVERY_MINUTE
    enabled: bool = False
    managed: bool = False
    repeat: int = INFINITE

    command: str = field(default_factory=str)

    _target: Optional[Callable[..., Any]] = None
    _args: List[Any] = field(default_factory=list)
    _kwargs: Dict[str, Any] = field(default_factory=dict)

    @property
    def key(self):
        return JobKey(self.uuid)

    @key.setter
    def key(self, value: JobKey) -> None:
        self.uuid = str(value)

    def set_infinite(self) -> None:
        self.repeat = INFINITE

    def set_target(self, target: Callable[..., Any], *args, **kwargs) -> None:
        self._target = target
        self._args = list(args)
        self._kwargs = kwargs

    def call_target(self) -> Any:
        if self._target is None:
            raise ValueError("Target callable is not set")
        return self._target(*self._args, **self._kwargs)

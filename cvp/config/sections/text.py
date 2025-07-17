# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime


def _local_tzname() -> str:
    name = datetime.now().astimezone().tzname()
    assert name is not None
    return name


@dataclass
class TextConfig:
    default_encoding: str = "utf-8"
    default_timezone: str = field(default_factory=lambda: _local_tzname())

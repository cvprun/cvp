# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from typing import Tuple
from uuid import uuid4


@unique
class MediaMode(StrEnum):
    file = auto()
    url = auto()
    manual = auto()


@dataclass
class MediaConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    opened: bool = False
    mode: MediaMode = MediaMode.file
    file: str = field(default_factory=str)
    cmds: str = field(default_factory=str)
    frame_width: int = 0
    frame_height: int = 0

    @property
    def is_file_mode(self) -> bool:
        return self.mode == MediaMode.file

    @property
    def is_url_mode(self) -> bool:
        return self.mode == MediaMode.url

    @property
    def is_manual_mode(self) -> bool:
        return self.mode == MediaMode.manual

    def set_file_mode(self) -> None:
        self.mode = MediaMode.file

    def set_url_mode(self) -> None:
        self.mode = MediaMode.url

    def set_manual_mode(self) -> None:
        self.mode = MediaMode.manual

    @property
    def frame_size(self) -> Tuple[int, int]:
        return self.frame_width, self.frame_height

    @frame_size.setter
    def frame_size(self, value: Tuple[int, int]) -> None:
        self.frame_width = value[0]
        self.frame_height = value[1]

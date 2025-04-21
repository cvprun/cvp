# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple
from uuid import uuid4

from cvp.variables import MEDIA_FRAME_HEIGHT, MEDIA_FRAME_WIDTH


@dataclass
class MediaConfig:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    opened: bool = False
    file: str = field(default_factory=str)
    frame_width: int = MEDIA_FRAME_WIDTH
    frame_height: int = MEDIA_FRAME_HEIGHT

    @property
    def frame_size(self) -> Tuple[int, int]:
        return self.frame_width, self.frame_height

    @frame_size.setter
    def frame_size(self, value: Tuple[int, int]) -> None:
        self.frame_width = value[0]
        self.frame_height = value[1]

    @property
    def valid_frame_size(self) -> bool:
        return 1 <= self.frame_width and 1 <= self.frame_height

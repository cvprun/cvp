# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from typing import Final, Sequence

from cvp.logging.logging import (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
    SEVERITY_NAME_WARNING,
    convert_level_number,
)
from cvp.palette.basic import BLUE, LIME, MAROON, RED, YELLOW
from cvp.types.colors import RGBA

LEVEL_NAMES: Final[Sequence[str]] = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)
DEFAULT_LEVEL_INDEX: Final[int] = LEVEL_NAMES.index(SEVERITY_NAME_NOTSET)


@dataclass
class Logs:
    level_names: list = field(default_factory=lambda: list(LEVEL_NAMES))
    level_index: int = DEFAULT_LEVEL_INDEX

    autoscroll: bool = False
    filter: str = field(default_factory=str)
    lines: int = 100
    dropdown_width: float = 20.0

    critical_color: RGBA = field(default_factory=lambda: (*MAROON, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    info_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    debug_color: RGBA = field(default_factory=lambda: (*BLUE, 1.0))

    @property
    def levelname(self) -> int:
        return self.level_names[self.level_index]

    @property
    def levelno(self) -> int:
        return convert_level_number(self.levelname)

    def get_level_color(self, level: int) -> RGBA:
        if ERROR < level <= CRITICAL:
            return self.critical_color
        elif WARNING < level <= ERROR:
            return self.error_color
        elif INFO < level <= WARNING:
            return self.warning_color
        elif DEBUG < level <= INFO:
            return self.info_color
        elif NOTSET < level <= DEBUG:
            return self.debug_color
        else:
            raise ValueError(f"Invalid level: {level}")

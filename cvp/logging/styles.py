# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from typing import Optional, overload

from cvp.logging.logging import (
    LEVEL_TO_NAME_MAPPING,
    NOTSET_LEVEL_NAME_INDEX,
    UNIQUE_LEVEL_NAMES,
    convert_level_number,
)
from cvp.palette.basic import BLUE, LIME, MAROON, RED, YELLOW
from cvp.types.colors import RGBA


@dataclass
class GuiLoggingStyle:
    level_index: int = NOTSET_LEVEL_NAME_INDEX

    lines: int = 1_000
    autoscroll: bool = False
    filter: str = field(default_factory=str)

    critical_color: RGBA = field(default_factory=lambda: (*MAROON, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    info_color: RGBA = field(default_factory=lambda: (*LIME, 1.0))
    debug_color: RGBA = field(default_factory=lambda: (*BLUE, 1.0))

    @property
    def level_name(self) -> str:
        return UNIQUE_LEVEL_NAMES[self.level_index]

    @level_name.setter
    def level_name(self, value: str) -> None:
        self.level_index = UNIQUE_LEVEL_NAMES.index(value)

    @property
    def level_number(self) -> int:
        return convert_level_number(self.level_name)

    @level_number.setter
    def level_number(self, value: int) -> None:
        self.level_name = LEVEL_TO_NAME_MAPPING[value]

    @overload
    def get_level_color(self, level: int) -> Optional[RGBA]: ...

    @overload
    def get_level_color(self, level: int, default: RGBA) -> RGBA: ...

    def get_level_color(
        self,
        level: int,
        default: Optional[RGBA] = None,
    ) -> Optional[RGBA]:
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
            return default

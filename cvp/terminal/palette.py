# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.colors.convert.uint32 import (
    rgb_to_uint32,
    rgba_to_uint32,
    uint32_to_rgb,
    uint32_to_rgba,
)
from cvp.palette.vga import (
    BLACK,
    BLUE,
    BRIGHT_BLACK,
    BRIGHT_BLUE,
    BRIGHT_CYAN,
    BRIGHT_GREEN,
    BRIGHT_MAGENTA,
    BRIGHT_RED,
    BRIGHT_WHITE,
    BRIGHT_YELLOW,
    CYAN,
    GREEN,
    MAGENTA,
    RED,
    WHITE,
    YELLOW,
)
from cvp.types.colors import RGB, RGBA


@dataclass
class TerminalPalette:
    black: int = field(default_factory=lambda: rgb_to_uint32(BLACK))
    red: int = field(default_factory=lambda: rgb_to_uint32(RED))
    green: int = field(default_factory=lambda: rgb_to_uint32(GREEN))
    yellow: int = field(default_factory=lambda: rgb_to_uint32(YELLOW))
    blue: int = field(default_factory=lambda: rgb_to_uint32(BLUE))
    magenta: int = field(default_factory=lambda: rgb_to_uint32(MAGENTA))
    cyan: int = field(default_factory=lambda: rgb_to_uint32(CYAN))
    white: int = field(default_factory=lambda: rgb_to_uint32(WHITE))

    bright_black: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_BLACK))
    bright_red: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_RED))
    bright_green: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_GREEN))
    bright_yellow: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_YELLOW))
    bright_blue: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_BLUE))
    bright_magenta: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_MAGENTA))
    bright_cyan: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_CYAN))
    bright_white: int = field(default_factory=lambda: rgb_to_uint32(BRIGHT_WHITE))

    # ----------------------------------------------------------------------------------

    @property
    def black_rgb(self) -> RGB:
        return uint32_to_rgb(self.black)

    @black_rgb.setter
    def black_rgb(self, value: RGB) -> None:
        self.black = rgb_to_uint32(value)

    @property
    def black_rgba(self) -> RGBA:
        return uint32_to_rgba(self.black)

    @black_rgba.setter
    def black_rgba(self, value: RGBA) -> None:
        self.black = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def red_rgb(self) -> RGB:
        return uint32_to_rgb(self.red)

    @red_rgb.setter
    def red_rgb(self, value: RGB) -> None:
        self.red = rgb_to_uint32(value)

    @property
    def red_rgba(self) -> RGBA:
        return uint32_to_rgba(self.red)

    @red_rgba.setter
    def red_rgba(self, value: RGBA) -> None:
        self.red = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def green_rgb(self) -> RGB:
        return uint32_to_rgb(self.green)

    @green_rgb.setter
    def green_rgb(self, value: RGB) -> None:
        self.green = rgb_to_uint32(value)

    @property
    def green_rgba(self) -> RGBA:
        return uint32_to_rgba(self.green)

    @green_rgba.setter
    def green_rgba(self, value: RGBA) -> None:
        self.green = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def yellow_rgb(self) -> RGB:
        return uint32_to_rgb(self.yellow)

    @yellow_rgb.setter
    def yellow_rgb(self, value: RGB) -> None:
        self.yellow = rgb_to_uint32(value)

    @property
    def yellow_rgba(self) -> RGBA:
        return uint32_to_rgba(self.yellow)

    @yellow_rgba.setter
    def yellow_rgba(self, value: RGBA) -> None:
        self.yellow = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def blue_rgb(self) -> RGB:
        return uint32_to_rgb(self.blue)

    @blue_rgb.setter
    def blue_rgb(self, value: RGB) -> None:
        self.blue = rgb_to_uint32(value)

    @property
    def blue_rgba(self) -> RGBA:
        return uint32_to_rgba(self.blue)

    @blue_rgba.setter
    def blue_rgba(self, value: RGBA) -> None:
        self.blue = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def magenta_rgb(self) -> RGB:
        return uint32_to_rgb(self.magenta)

    @magenta_rgb.setter
    def magenta_rgb(self, value: RGB) -> None:
        self.magenta = rgb_to_uint32(value)

    @property
    def magenta_rgba(self) -> RGBA:
        return uint32_to_rgba(self.magenta)

    @magenta_rgba.setter
    def magenta_rgba(self, value: RGBA) -> None:
        self.magenta = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def cyan_rgb(self) -> RGB:
        return uint32_to_rgb(self.cyan)

    @cyan_rgb.setter
    def cyan_rgb(self, value: RGB) -> None:
        self.cyan = rgb_to_uint32(value)

    @property
    def cyan_rgba(self) -> RGBA:
        return uint32_to_rgba(self.cyan)

    @cyan_rgba.setter
    def cyan_rgba(self, value: RGBA) -> None:
        self.cyan = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def white_rgb(self) -> RGB:
        return uint32_to_rgb(self.white)

    @white_rgb.setter
    def white_rgb(self, value: RGB) -> None:
        self.white = rgb_to_uint32(value)

    @property
    def white_rgba(self) -> RGBA:
        return uint32_to_rgba(self.white)

    @white_rgba.setter
    def white_rgba(self, value: RGBA) -> None:
        self.white = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_black_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_black)

    @bright_black_rgb.setter
    def bright_black_rgb(self, value: RGB) -> None:
        self.bright_black = rgb_to_uint32(value)

    @property
    def bright_black_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_black)

    @bright_black_rgba.setter
    def bright_black_rgba(self, value: RGBA) -> None:
        self.bright_black = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_red_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_red)

    @bright_red_rgb.setter
    def bright_red_rgb(self, value: RGB) -> None:
        self.bright_red = rgb_to_uint32(value)

    @property
    def bright_red_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_red)

    @bright_red_rgba.setter
    def bright_red_rgba(self, value: RGBA) -> None:
        self.bright_red = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_green_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_green)

    @bright_green_rgb.setter
    def bright_green_rgb(self, value: RGB) -> None:
        self.bright_green = rgb_to_uint32(value)

    @property
    def bright_green_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_green)

    @bright_green_rgba.setter
    def bright_green_rgba(self, value: RGBA) -> None:
        self.bright_green = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_yellow_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_yellow)

    @bright_yellow_rgb.setter
    def bright_yellow_rgb(self, value: RGB) -> None:
        self.bright_yellow = rgb_to_uint32(value)

    @property
    def bright_yellow_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_yellow)

    @bright_yellow_rgba.setter
    def bright_yellow_rgba(self, value: RGBA) -> None:
        self.bright_yellow = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_blue_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_blue)

    @bright_blue_rgb.setter
    def bright_blue_rgb(self, value: RGB) -> None:
        self.bright_blue = rgb_to_uint32(value)

    @property
    def bright_blue_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_blue)

    @bright_blue_rgba.setter
    def bright_blue_rgba(self, value: RGBA) -> None:
        self.bright_blue = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_magenta_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_magenta)

    @bright_magenta_rgb.setter
    def bright_magenta_rgb(self, value: RGB) -> None:
        self.bright_magenta = rgb_to_uint32(value)

    @property
    def bright_magenta_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_magenta)

    @bright_magenta_rgba.setter
    def bright_magenta_rgba(self, value: RGBA) -> None:
        self.bright_magenta = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_cyan_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_cyan)

    @bright_cyan_rgb.setter
    def bright_cyan_rgb(self, value: RGB) -> None:
        self.bright_cyan = rgb_to_uint32(value)

    @property
    def bright_cyan_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_cyan)

    @bright_cyan_rgba.setter
    def bright_cyan_rgba(self, value: RGBA) -> None:
        self.bright_cyan = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

    @property
    def bright_white_rgb(self) -> RGB:
        return uint32_to_rgb(self.bright_white)

    @bright_white_rgb.setter
    def bright_white_rgb(self, value: RGB) -> None:
        self.bright_white = rgb_to_uint32(value)

    @property
    def bright_white_rgba(self) -> RGBA:
        return uint32_to_rgba(self.bright_white)

    @bright_white_rgba.setter
    def bright_white_rgba(self, value: RGBA) -> None:
        self.bright_white = rgba_to_uint32(value)

    # ----------------------------------------------------------------------------------

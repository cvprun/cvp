# -*- coding: utf-8 -*-

from typing import Literal, Optional, Sequence, Tuple, Union

from pygame import display as pg_display
from pygame.constants import FULLSCREEN
from pygame.surface import Surface
from pygame.typing import RectLike
from pygame.window import Window

from cvp.pygame.types import Coordinate, SequenceProtocol


class Displayable:
    @staticmethod
    def display_init():
        return pg_display.init()

    @staticmethod
    def display_quit():
        return pg_display.quit()

    @staticmethod
    def display_get_init():
        return pg_display.get_init()

    @staticmethod
    def display_set_mode(
        size: Sequence[float] = (0, 0),
        flags=0,
        depth=0,
        display=0,
        vsync=0,
    ):
        assert isinstance(size, SequenceProtocol)
        return pg_display.set_mode(size, flags, depth, display, vsync)

    @staticmethod
    def display_get_surface():
        return pg_display.get_surface()

    @staticmethod
    def display_flip():
        return pg_display.flip()

    @staticmethod
    def display_update():
        return pg_display.update()

    @staticmethod
    def display_update_with_rectangle(rectangle: RectLike):
        return pg_display.update(rectangle)

    @staticmethod
    def display_update_with_coords(xy: Coordinate, wh: Coordinate):
        return pg_display.update(xy, wh)

    @staticmethod
    def display_update_with_raws(x: int, y: int, w: int, h: int):
        return pg_display.update(x, y, w, h)

    @staticmethod
    def display_get_driver():
        return pg_display.get_driver()

    @staticmethod
    def display_info():
        return pg_display.Info()

    @staticmethod
    def display_size() -> Tuple[int, int]:
        display_info = pg_display.Info()
        return display_info.current_w, display_info.current_h

    @staticmethod
    def display_get_wm_info():
        return pg_display.get_wm_info()

    @staticmethod
    def display_get_desktop_sizes():
        return pg_display.get_desktop_sizes()

    @staticmethod
    def display_list_modes(depth=0, flags=FULLSCREEN, display=0):
        return pg_display.list_modes(depth, flags, display)

    @staticmethod
    def display_mode_ok(size: Sequence[int], flags=0, depth=0, display=0):
        assert isinstance(size, SequenceProtocol)
        return pg_display.mode_ok(size, flags, depth, display)

    @staticmethod
    def display_gl_get_attribute(flag: int):
        return pg_display.gl_get_attribute(flag)

    @staticmethod
    def display_gl_set_attribute(flag: int, value: int):
        return pg_display.gl_set_attribute(flag, value)

    @staticmethod
    def display_get_active():
        return pg_display.get_active()

    @staticmethod
    def display_iconify():
        return pg_display.iconify()

    @staticmethod
    def display_toggle_fullscreen():
        return pg_display.toggle_fullscreen()

    @staticmethod
    def display_set_gamma(red: float, green: float, blue: float):
        return pg_display.set_gamma(red, green, blue)

    @staticmethod
    def display_set_gamma_ramp(
        red: Sequence[int],
        green: Sequence[int],
        blue: Sequence[int],
    ):
        assert isinstance(red, SequenceProtocol)
        assert isinstance(green, SequenceProtocol)
        assert isinstance(blue, SequenceProtocol)
        return pg_display.set_gamma_ramp(red, green, blue)

    @staticmethod
    def display_set_icon(surface: Surface):
        return pg_display.set_icon(surface)

    @staticmethod
    def display_set_caption(title: str, icon_title: Optional[str] = None):
        if icon_title:
            return pg_display.set_caption(title, icon_title)
        else:
            return pg_display.set_caption(title)

    @staticmethod
    def display_get_caption():
        return pg_display.get_caption()

    @staticmethod
    def display_set_palette(palette: Sequence[Union[int, str, Sequence[int]]]):
        assert isinstance(palette, SequenceProtocol)
        return pg_display.set_palette(palette)

    @staticmethod
    def display_get_num_displays():
        return pg_display.get_num_displays()

    @staticmethod
    def display_get_window_size():
        return pg_display.get_window_size()

    @staticmethod
    def display_get_allow_screensaver():
        return pg_display.get_allow_screensaver()

    @staticmethod
    def display_set_allow_screensaver(value=True):
        return pg_display.set_allow_screensaver(value)

    @staticmethod
    def display_is_fullscreen():
        return pg_display.is_fullscreen()

    @staticmethod
    def display_is_vsync():
        return pg_display.is_vsync()

    @staticmethod
    def display_get_current_refresh_rate():
        return pg_display.get_current_refresh_rate()

    @staticmethod
    def display_get_desktop_refresh_rates():
        return pg_display.get_desktop_refresh_rates()

    @staticmethod
    def display_message_box(
        title: str,
        message: Optional[str] = None,
        message_type: Literal["info", "warn", "error"] = "info",
        parent_window: Optional[Window] = None,
        buttons: Sequence[str] = ("OK",),
        return_button=0,
        escape_button: Optional[int] = None,
    ):
        assert isinstance(buttons, SequenceProtocol)
        return pg_display.message_box(
            title,
            message,
            message_type,
            parent_window,
            buttons,
            return_button,
            escape_button,
        )

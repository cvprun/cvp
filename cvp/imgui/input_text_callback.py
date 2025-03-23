# -*- coding: utf-8 -*-

from warnings import warn

import pygame
from imgui_bundle import imgui
from pygame.key import get_pressed

from cvp.imgui.flags.input_text import CALLBACK_ALWAYS
from cvp.imgui.version import version


def _copy_selection(data: imgui.InputTextCallbackData) -> None:
    if not data.has_selection():
        return

    if version() <= (2, 0, 0):
        message = "Segfault occurs when accessing 'data.buffer' in pyimgui 2.0.0"
        warn(message, RuntimeWarning)

    buffer = data.buf
    """
    [WARNING] Segmentation Fault
    """

    begin = data.selection_start
    end = data.selection_end
    selected_text = buffer[begin:end]
    assert isinstance(selected_text, str)
    pygame.scrap.put_text(selected_text)


def _remove_selection(data: imgui.InputTextCallbackData) -> None:
    begin = data.selection_start
    end = data.selection_end
    data.delete_chars(begin, end - begin)
    data.cursor_pos = begin


def _cut_selection(data: imgui.InputTextCallbackData) -> None:
    if not data.has_selection():
        return

    _copy_selection(data)
    _remove_selection(data)


def _paste_selection(data: imgui.InputTextCallbackData) -> None:
    clipboard_text = pygame.scrap.get_text()
    if not clipboard_text:
        return

    if data.has_selection():
        _remove_selection(data)

    data.insert_chars(data.cursor_pos, clipboard_text)


def input_text_resize_callback(data: imgui.InputTextCallbackData) -> int:
    assert data.flags & CALLBACK_ALWAYS
    keys = get_pressed()

    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        if keys[pygame.K_x]:
            _cut_selection(data)
        elif keys[pygame.K_c]:
            _copy_selection(data)
        elif keys[pygame.K_v]:
            _paste_selection(data)
    return 0

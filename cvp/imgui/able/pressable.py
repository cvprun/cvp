# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def _imgui_is_pressed(key: int) -> bool:
    return imgui.is_key_pressed(imgui.get_key_index(key))


class Pressable:
    @staticmethod
    def imgui_is_pressed(key: int) -> bool:
        return _imgui_is_pressed(key)

    @staticmethod
    def imgui_is_pressed_tab() -> bool:
        return _imgui_is_pressed(imgui.KEY_TAB)

    @staticmethod
    def imgui_is_pressed_left_arrow() -> bool:
        return _imgui_is_pressed(imgui.KEY_LEFT_ARROW)

    @staticmethod
    def imgui_is_pressed_right_arrow() -> bool:
        return _imgui_is_pressed(imgui.KEY_RIGHT_ARROW)

    @staticmethod
    def imgui_is_pressed_up_arrow() -> bool:
        return _imgui_is_pressed(imgui.KEY_UP_ARROW)

    @staticmethod
    def imgui_is_pressed_down_arrow() -> bool:
        return _imgui_is_pressed(imgui.KEY_DOWN_ARROW)

    @staticmethod
    def imgui_is_pressed_page_up() -> bool:
        return _imgui_is_pressed(imgui.KEY_PAGE_UP)

    @staticmethod
    def imgui_is_pressed_page_down() -> bool:
        return _imgui_is_pressed(imgui.KEY_PAGE_DOWN)

    @staticmethod
    def imgui_is_pressed_home() -> bool:
        return _imgui_is_pressed(imgui.KEY_HOME)

    @staticmethod
    def imgui_is_pressed_end() -> bool:
        return _imgui_is_pressed(imgui.KEY_END)

    @staticmethod
    def imgui_is_pressed_insert() -> bool:
        return _imgui_is_pressed(imgui.KEY_INSERT)

    @staticmethod
    def imgui_is_pressed_delete() -> bool:
        return _imgui_is_pressed(imgui.KEY_DELETE)

    @staticmethod
    def imgui_is_pressed_backspace() -> bool:
        return _imgui_is_pressed(imgui.KEY_BACKSPACE)

    @staticmethod
    def imgui_is_pressed_space() -> bool:
        return _imgui_is_pressed(imgui.KEY_SPACE)

    @staticmethod
    def imgui_is_pressed_enter() -> bool:
        return _imgui_is_pressed(imgui.KEY_ENTER)

    @staticmethod
    def imgui_is_pressed_escape() -> bool:
        return _imgui_is_pressed(imgui.KEY_ESCAPE)

    @staticmethod
    def imgui_is_pressed_pad_enter() -> bool:
        return _imgui_is_pressed(imgui.KEY_PAD_ENTER)

    @staticmethod
    def imgui_is_pressed_a() -> bool:
        return _imgui_is_pressed(imgui.KEY_A)

    @staticmethod
    def imgui_is_pressed_c() -> bool:
        return _imgui_is_pressed(imgui.KEY_C)

    @staticmethod
    def imgui_is_pressed_v() -> bool:
        return _imgui_is_pressed(imgui.KEY_V)

    @staticmethod
    def imgui_is_pressed_x() -> bool:
        return _imgui_is_pressed(imgui.KEY_X)

    @staticmethod
    def imgui_is_pressed_y() -> bool:
        return _imgui_is_pressed(imgui.KEY_Y)

    @staticmethod
    def imgui_is_pressed_z() -> bool:
        return _imgui_is_pressed(imgui.KEY_Z)

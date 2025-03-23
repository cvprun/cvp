# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def _imgui_is_pressed(key: imgui.Key) -> bool:
    return imgui.is_key_pressed(key)


class Pressable:
    @staticmethod
    def imgui_is_pressed(key: imgui.Key) -> bool:
        return _imgui_is_pressed(key)

    @staticmethod
    def imgui_is_pressed_tab() -> bool:
        return _imgui_is_pressed(imgui.Key.tab)

    @staticmethod
    def imgui_is_pressed_left_arrow() -> bool:
        return _imgui_is_pressed(imgui.Key.left_arrow)

    @staticmethod
    def imgui_is_pressed_right_arrow() -> bool:
        return _imgui_is_pressed(imgui.Key.right_arrow)

    @staticmethod
    def imgui_is_pressed_up_arrow() -> bool:
        return _imgui_is_pressed(imgui.Key.up_arrow)

    @staticmethod
    def imgui_is_pressed_down_arrow() -> bool:
        return _imgui_is_pressed(imgui.Key.down_arrow)

    @staticmethod
    def imgui_is_pressed_page_up() -> bool:
        return _imgui_is_pressed(imgui.Key.page_up)

    @staticmethod
    def imgui_is_pressed_page_down() -> bool:
        return _imgui_is_pressed(imgui.Key.page_down)

    @staticmethod
    def imgui_is_pressed_home() -> bool:
        return _imgui_is_pressed(imgui.Key.home)

    @staticmethod
    def imgui_is_pressed_end() -> bool:
        return _imgui_is_pressed(imgui.Key.end)

    @staticmethod
    def imgui_is_pressed_insert() -> bool:
        return _imgui_is_pressed(imgui.Key.insert)

    @staticmethod
    def imgui_is_pressed_delete() -> bool:
        return _imgui_is_pressed(imgui.Key.delete)

    @staticmethod
    def imgui_is_pressed_backspace() -> bool:
        return _imgui_is_pressed(imgui.Key.backspace)

    @staticmethod
    def imgui_is_pressed_space() -> bool:
        return _imgui_is_pressed(imgui.Key.space)

    @staticmethod
    def imgui_is_pressed_enter() -> bool:
        return _imgui_is_pressed(imgui.Key.enter)

    @staticmethod
    def imgui_is_pressed_escape() -> bool:
        return _imgui_is_pressed(imgui.Key.escape)

    @staticmethod
    def imgui_is_pressed_pad_enter() -> bool:
        return _imgui_is_pressed(imgui.Key.keypad_enter)

    @staticmethod
    def imgui_is_pressed_a() -> bool:
        return _imgui_is_pressed(imgui.Key.a)

    @staticmethod
    def imgui_is_pressed_c() -> bool:
        return _imgui_is_pressed(imgui.Key.c)

    @staticmethod
    def imgui_is_pressed_v() -> bool:
        return _imgui_is_pressed(imgui.Key.v)

    @staticmethod
    def imgui_is_pressed_x() -> bool:
        return _imgui_is_pressed(imgui.Key.x)

    @staticmethod
    def imgui_is_pressed_y() -> bool:
        return _imgui_is_pressed(imgui.Key.y)

    @staticmethod
    def imgui_is_pressed_z() -> bool:
        return _imgui_is_pressed(imgui.Key.z)

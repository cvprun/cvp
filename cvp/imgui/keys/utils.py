# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def _is_key_down(key: imgui.Key) -> bool:
    return imgui.is_key_down(key)


def shift_down() -> bool:
    return _is_key_down(imgui.Key.left_shift) or _is_key_down(imgui.Key.right_shift)


def ctrl_down() -> bool:
    return _is_key_down(imgui.Key.left_ctrl) or _is_key_down(imgui.Key.right_ctrl)


def alt_down() -> bool:
    return _is_key_down(imgui.Key.left_alt) or _is_key_down(imgui.Key.right_alt)


def super_down() -> bool:
    return _is_key_down(imgui.Key.left_super) or _is_key_down(imgui.Key.right_super)


def only_shift_down() -> bool:
    return shift_down() and not ctrl_down() and not alt_down() and not super_down()


def only_ctrl_down() -> bool:
    return not shift_down() and ctrl_down() and not alt_down() and not super_down()


def only_alt_down() -> bool:
    return not shift_down() and not ctrl_down() and alt_down() and not super_down()


def only_super_down() -> bool:
    return not shift_down() and not ctrl_down() and not alt_down() and super_down()


def only_shift_ctrl_down() -> bool:
    return shift_down() and ctrl_down() and not alt_down() and not super_down()


def only_ctrl_alt_down() -> bool:
    return not shift_down() and ctrl_down() and alt_down() and not super_down()


def only_shift_alt_down() -> bool:
    return shift_down() and not ctrl_down() and alt_down() and not super_down()


def only_shift_ctrl_alt_down() -> bool:
    return shift_down() and ctrl_down() and alt_down() and not super_down()


def is_key_pressed(key: imgui.Key, repeat=True) -> bool:
    return imgui.is_key_pressed(key, repeat)


def enter_pressed() -> bool:
    return is_key_pressed(imgui.Key.enter) or is_key_pressed(imgui.Key.keypad_enter)


def only_shift_enter_pressed() -> bool:
    return only_shift_down() and enter_pressed()

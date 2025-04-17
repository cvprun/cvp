# -*- coding: utf-8 -*-

from enum import IntFlag
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


class KeyFlags(IntFlag):
    none = imgui.Key.none.value
    tab = imgui.Key.tab.value
    left_arrow = imgui.Key.left_arrow.value
    right_arrow = imgui.Key.right_arrow.value
    up_arrow = imgui.Key.up_arrow.value
    down_arrow = imgui.Key.down_arrow.value
    page_up = imgui.Key.page_up.value
    page_down = imgui.Key.page_down.value
    home = imgui.Key.home.value
    end = imgui.Key.end.value
    insert = imgui.Key.insert.value
    delete = imgui.Key.delete.value
    backspace = imgui.Key.backspace.value
    space = imgui.Key.space.value
    enter = imgui.Key.enter.value
    escape = imgui.Key.escape.value
    left_ctrl = imgui.Key.left_ctrl.value
    left_shift = imgui.Key.left_shift.value
    left_alt = imgui.Key.left_alt.value
    left_super = imgui.Key.left_super.value
    right_ctrl = imgui.Key.right_ctrl.value
    right_shift = imgui.Key.right_shift.value
    right_alt = imgui.Key.right_alt.value
    right_super = imgui.Key.right_super.value
    menu = imgui.Key.menu.value

    # noinspection PyProtectedMember
    _0 = imgui.Key._0.value
    # noinspection PyProtectedMember
    _1 = imgui.Key._1.value
    # noinspection PyProtectedMember
    _2 = imgui.Key._2.value
    # noinspection PyProtectedMember
    _3 = imgui.Key._3.value
    # noinspection PyProtectedMember
    _4 = imgui.Key._4.value
    # noinspection PyProtectedMember
    _5 = imgui.Key._5.value
    # noinspection PyProtectedMember
    _6 = imgui.Key._6.value
    # noinspection PyProtectedMember
    _7 = imgui.Key._7.value
    # noinspection PyProtectedMember
    _8 = imgui.Key._8.value
    # noinspection PyProtectedMember
    _9 = imgui.Key._9.value

    a = imgui.Key.a.value
    b = imgui.Key.b.value
    c = imgui.Key.c.value
    d = imgui.Key.d.value
    e = imgui.Key.e.value
    f = imgui.Key.f.value
    g = imgui.Key.g.value
    h = imgui.Key.h.value
    i = imgui.Key.i.value
    j = imgui.Key.j.value
    k = imgui.Key.k.value
    l = imgui.Key.l.value  # noqa: E741
    m = imgui.Key.m.value
    n = imgui.Key.n.value
    o = imgui.Key.o.value
    p = imgui.Key.p.value
    q = imgui.Key.q.value
    r = imgui.Key.r.value
    s = imgui.Key.s.value
    t = imgui.Key.t.value
    u = imgui.Key.u.value
    v = imgui.Key.v.value
    w = imgui.Key.w.value
    x = imgui.Key.x.value
    y = imgui.Key.y.value
    z = imgui.Key.z.value
    f1 = imgui.Key.f1.value
    f2 = imgui.Key.f2.value
    f3 = imgui.Key.f3.value
    f4 = imgui.Key.f4.value
    f5 = imgui.Key.f5.value
    f6 = imgui.Key.f6.value
    f7 = imgui.Key.f7.value
    f8 = imgui.Key.f8.value
    f9 = imgui.Key.f9.value
    f10 = imgui.Key.f10.value
    f11 = imgui.Key.f11.value
    f12 = imgui.Key.f12.value
    f13 = imgui.Key.f13.value
    f14 = imgui.Key.f14.value
    f15 = imgui.Key.f15.value
    f16 = imgui.Key.f16.value
    f17 = imgui.Key.f17.value
    f18 = imgui.Key.f18.value
    f19 = imgui.Key.f19.value
    f20 = imgui.Key.f20.value
    f21 = imgui.Key.f21.value
    f22 = imgui.Key.f22.value
    f23 = imgui.Key.f23.value
    f24 = imgui.Key.f24.value
    apostrophe = imgui.Key.apostrophe.value
    comma = imgui.Key.comma.value
    minus = imgui.Key.minus.value
    period = imgui.Key.period.value
    slash = imgui.Key.slash.value
    semicolon = imgui.Key.semicolon.value
    equal = imgui.Key.equal.value
    left_bracket = imgui.Key.left_bracket.value
    backslash = imgui.Key.backslash.value
    right_bracket = imgui.Key.right_bracket.value
    grave_accent = imgui.Key.grave_accent.value
    caps_lock = imgui.Key.caps_lock.value
    scroll_lock = imgui.Key.scroll_lock.value
    num_lock = imgui.Key.num_lock.value
    print_screen = imgui.Key.print_screen.value
    pause = imgui.Key.pause.value
    keypad0 = imgui.Key.keypad0.value
    keypad1 = imgui.Key.keypad1.value
    keypad2 = imgui.Key.keypad2.value
    keypad3 = imgui.Key.keypad3.value
    keypad4 = imgui.Key.keypad4.value
    keypad5 = imgui.Key.keypad5.value
    keypad6 = imgui.Key.keypad6.value
    keypad7 = imgui.Key.keypad7.value
    keypad8 = imgui.Key.keypad8.value
    keypad9 = imgui.Key.keypad9.value
    keypad_decimal = imgui.Key.keypad_decimal.value
    keypad_divide = imgui.Key.keypad_divide.value
    keypad_multiply = imgui.Key.keypad_multiply.value
    keypad_subtract = imgui.Key.keypad_subtract.value
    keypad_add = imgui.Key.keypad_add.value
    keypad_enter = imgui.Key.keypad_enter.value
    keypad_equal = imgui.Key.keypad_equal.value
    app_back = imgui.Key.app_back.value
    app_forward = imgui.Key.app_forward.value

    # Gamepad (some of those are analog values, 0.0 to 1.0)
    gamepad_start = imgui.Key.gamepad_start.value
    gamepad_back = imgui.Key.gamepad_back.value
    gamepad_face_left = imgui.Key.gamepad_face_left.value
    gamepad_face_right = imgui.Key.gamepad_face_right.value
    gamepad_face_up = imgui.Key.gamepad_face_up.value
    gamepad_face_down = imgui.Key.gamepad_face_down.value
    gamepad_dpad_left = imgui.Key.gamepad_dpad_left.value
    gamepad_dpad_right = imgui.Key.gamepad_dpad_right.value
    gamepad_dpad_up = imgui.Key.gamepad_dpad_up.value
    gamepad_dpad_down = imgui.Key.gamepad_dpad_down.value
    gamepad_l1 = imgui.Key.gamepad_l1.value
    gamepad_r1 = imgui.Key.gamepad_r1.value
    gamepad_l2 = imgui.Key.gamepad_l2.value
    gamepad_r2 = imgui.Key.gamepad_r2.value
    gamepad_l3 = imgui.Key.gamepad_l3.value
    gamepad_r3 = imgui.Key.gamepad_r3.value
    gamepad_l_stick_left = imgui.Key.gamepad_l_stick_left.value
    gamepad_l_stick_right = imgui.Key.gamepad_l_stick_right.value
    gamepad_l_stick_up = imgui.Key.gamepad_l_stick_up.value
    gamepad_l_stick_down = imgui.Key.gamepad_l_stick_down.value
    gamepad_r_stick_left = imgui.Key.gamepad_r_stick_left.value
    gamepad_r_stick_right = imgui.Key.gamepad_r_stick_right.value
    gamepad_r_stick_up = imgui.Key.gamepad_r_stick_up.value
    gamepad_r_stick_down = imgui.Key.gamepad_r_stick_down.value

    # ImGuiKey_MouseLeft
    mouse_left = imgui.Key.mouse_left.value
    mouse_right = imgui.Key.mouse_right.value
    mouse_middle = imgui.Key.mouse_middle.value
    mouse_x1 = imgui.Key.mouse_x1.value
    mouse_x2 = imgui.Key.mouse_x2.value
    mouse_wheel_x = imgui.Key.mouse_wheel_x.value
    mouse_wheel_y = imgui.Key.mouse_wheel_y.value

    # ImGuiKey_ReservedForModCtrl
    reserved_for_mod_ctrl = imgui.Key.reserved_for_mod_ctrl.value
    reserved_for_mod_shift = imgui.Key.reserved_for_mod_shift.value
    reserved_for_mod_alt = imgui.Key.reserved_for_mod_alt.value
    reserved_for_mod_super = imgui.Key.reserved_for_mod_super.value
    named_key_end = imgui.Key.named_key_end.value

    # Keyboard Modifiers
    mod_none = imgui.Key.mod_none.value
    mod_ctrl = imgui.Key.mod_ctrl.value
    mod_shift = imgui.Key.mod_shift.value
    mod_alt = imgui.Key.mod_alt.value
    mod_super = imgui.Key.mod_super.value
    mod_mask_ = imgui.Key.mod_mask_.value


NONE: Final[int] = int(KeyFlags.none)
TAB: Final[int] = int(KeyFlags.tab)
LEFT_ARROW: Final[int] = int(KeyFlags.left_arrow)
RIGHT_ARROW: Final[int] = int(KeyFlags.right_arrow)
UP_ARROW: Final[int] = int(KeyFlags.up_arrow)
DOWN_ARROW: Final[int] = int(KeyFlags.down_arrow)
PAGE_UP: Final[int] = int(KeyFlags.page_up)
PAGE_DOWN: Final[int] = int(KeyFlags.page_down)
HOME: Final[int] = int(KeyFlags.home)
END: Final[int] = int(KeyFlags.end)
INSERT: Final[int] = int(KeyFlags.insert)
DELETE: Final[int] = int(KeyFlags.delete)
BACKSPACE: Final[int] = int(KeyFlags.backspace)
SPACE: Final[int] = int(KeyFlags.space)
ENTER: Final[int] = int(KeyFlags.enter)
ESCAPE: Final[int] = int(KeyFlags.escape)
LEFT_CTRL: Final[int] = int(KeyFlags.left_ctrl)
LEFT_SHIFT: Final[int] = int(KeyFlags.left_shift)
LEFT_ALT: Final[int] = int(KeyFlags.left_alt)
LEFT_SUPER: Final[int] = int(KeyFlags.left_super)
RIGHT_CTRL: Final[int] = int(KeyFlags.right_ctrl)
RIGHT_SHIFT: Final[int] = int(KeyFlags.right_shift)
RIGHT_ALT: Final[int] = int(KeyFlags.right_alt)
RIGHT_SUPER: Final[int] = int(KeyFlags.right_super)
MENU: Final[int] = int(KeyFlags.menu)

# noinspection PyProtectedMember
K_0: Final[int] = int(KeyFlags._0)
# noinspection PyProtectedMember
K_1: Final[int] = int(KeyFlags._1)
# noinspection PyProtectedMember
K_2: Final[int] = int(KeyFlags._2)
# noinspection PyProtectedMember
K_3: Final[int] = int(KeyFlags._3)
# noinspection PyProtectedMember
K_4: Final[int] = int(KeyFlags._4)
# noinspection PyProtectedMember
K_5: Final[int] = int(KeyFlags._5)
# noinspection PyProtectedMember
K_6: Final[int] = int(KeyFlags._6)
# noinspection PyProtectedMember
K_7: Final[int] = int(KeyFlags._7)
# noinspection PyProtectedMember
K_8: Final[int] = int(KeyFlags._8)
# noinspection PyProtectedMember
K_9: Final[int] = int(KeyFlags._9)

A: Final[int] = int(KeyFlags.a)
B: Final[int] = int(KeyFlags.b)
C: Final[int] = int(KeyFlags.c)
D: Final[int] = int(KeyFlags.d)
E: Final[int] = int(KeyFlags.e)
F: Final[int] = int(KeyFlags.f)
G: Final[int] = int(KeyFlags.g)
H: Final[int] = int(KeyFlags.h)
I: Final[int] = int(KeyFlags.i)
J: Final[int] = int(KeyFlags.j)
K: Final[int] = int(KeyFlags.k)
L: Final[int] = int(KeyFlags.l)
M: Final[int] = int(KeyFlags.m)
N: Final[int] = int(KeyFlags.n)
O: Final[int] = int(KeyFlags.o)
P: Final[int] = int(KeyFlags.p)
Q: Final[int] = int(KeyFlags.q)
R: Final[int] = int(KeyFlags.r)
S: Final[int] = int(KeyFlags.s)
T: Final[int] = int(KeyFlags.t)
U: Final[int] = int(KeyFlags.u)
V: Final[int] = int(KeyFlags.v)
W: Final[int] = int(KeyFlags.w)
X: Final[int] = int(KeyFlags.x)
Y: Final[int] = int(KeyFlags.y)
Z: Final[int] = int(KeyFlags.z)
F1: Final[int] = int(KeyFlags.f1)
F2: Final[int] = int(KeyFlags.f2)
F3: Final[int] = int(KeyFlags.f3)
F4: Final[int] = int(KeyFlags.f4)
F5: Final[int] = int(KeyFlags.f5)
F6: Final[int] = int(KeyFlags.f6)
F7: Final[int] = int(KeyFlags.f7)
F8: Final[int] = int(KeyFlags.f8)
F9: Final[int] = int(KeyFlags.f9)
F10: Final[int] = int(KeyFlags.f10)
F11: Final[int] = int(KeyFlags.f11)
F12: Final[int] = int(KeyFlags.f12)
F13: Final[int] = int(KeyFlags.f13)
F14: Final[int] = int(KeyFlags.f14)
F15: Final[int] = int(KeyFlags.f15)
F16: Final[int] = int(KeyFlags.f16)
F17: Final[int] = int(KeyFlags.f17)
F18: Final[int] = int(KeyFlags.f18)
F19: Final[int] = int(KeyFlags.f19)
F20: Final[int] = int(KeyFlags.f20)
F21: Final[int] = int(KeyFlags.f21)
F22: Final[int] = int(KeyFlags.f22)
F23: Final[int] = int(KeyFlags.f23)
F24: Final[int] = int(KeyFlags.f24)
APOSTROPHE: Final[int] = int(KeyFlags.apostrophe)
COMMA: Final[int] = int(KeyFlags.comma)
MINUS: Final[int] = int(KeyFlags.minus)
PERIOD: Final[int] = int(KeyFlags.period)
SLASH: Final[int] = int(KeyFlags.slash)
SEMICOLON: Final[int] = int(KeyFlags.semicolon)
EQUAL: Final[int] = int(KeyFlags.equal)
LEFT_BRACKET: Final[int] = int(KeyFlags.left_bracket)
BACKSLASH: Final[int] = int(KeyFlags.backslash)
RIGHT_BRACKET: Final[int] = int(KeyFlags.right_bracket)
GRAVE_ACCENT: Final[int] = int(KeyFlags.grave_accent)
CAPS_LOCK: Final[int] = int(KeyFlags.caps_lock)
SCROLL_LOCK: Final[int] = int(KeyFlags.scroll_lock)
NUM_LOCK: Final[int] = int(KeyFlags.num_lock)
PRINT_SCREEN: Final[int] = int(KeyFlags.print_screen)
PAUSE: Final[int] = int(KeyFlags.pause)
KEYPAD0: Final[int] = int(KeyFlags.keypad0)
KEYPAD1: Final[int] = int(KeyFlags.keypad1)
KEYPAD2: Final[int] = int(KeyFlags.keypad2)
KEYPAD3: Final[int] = int(KeyFlags.keypad3)
KEYPAD4: Final[int] = int(KeyFlags.keypad4)
KEYPAD5: Final[int] = int(KeyFlags.keypad5)
KEYPAD6: Final[int] = int(KeyFlags.keypad6)
KEYPAD7: Final[int] = int(KeyFlags.keypad7)
KEYPAD8: Final[int] = int(KeyFlags.keypad8)
KEYPAD9: Final[int] = int(KeyFlags.keypad9)
KEYPAD_DECIMAL: Final[int] = int(KeyFlags.keypad_decimal)
KEYPAD_DIVIDE: Final[int] = int(KeyFlags.keypad_divide)
KEYPAD_MULTIPLY: Final[int] = int(KeyFlags.keypad_multiply)
KEYPAD_SUBTRACT: Final[int] = int(KeyFlags.keypad_subtract)
KEYPAD_ADD: Final[int] = int(KeyFlags.keypad_add)
KEYPAD_ENTER: Final[int] = int(KeyFlags.keypad_enter)
KEYPAD_EQUAL: Final[int] = int(KeyFlags.keypad_equal)
APP_BACK: Final[int] = int(KeyFlags.app_back)
APP_FORWARD: Final[int] = int(KeyFlags.app_forward)
GAMEPAD_START: Final[int] = int(KeyFlags.gamepad_start)
GAMEPAD_BACK: Final[int] = int(KeyFlags.gamepad_back)
GAMEPAD_FACE_LEFT: Final[int] = int(KeyFlags.gamepad_face_left)
GAMEPAD_FACE_RIGHT: Final[int] = int(KeyFlags.gamepad_face_right)
GAMEPAD_FACE_UP: Final[int] = int(KeyFlags.gamepad_face_up)
GAMEPAD_FACE_DOWN: Final[int] = int(KeyFlags.gamepad_face_down)
GAMEPAD_DPAD_LEFT: Final[int] = int(KeyFlags.gamepad_dpad_left)
GAMEPAD_DPAD_RIGHT: Final[int] = int(KeyFlags.gamepad_dpad_right)
GAMEPAD_DPAD_UP: Final[int] = int(KeyFlags.gamepad_dpad_up)
GAMEPAD_DPAD_DOWN: Final[int] = int(KeyFlags.gamepad_dpad_down)
GAMEPAD_L1: Final[int] = int(KeyFlags.gamepad_l1)
GAMEPAD_R1: Final[int] = int(KeyFlags.gamepad_r1)
GAMEPAD_L2: Final[int] = int(KeyFlags.gamepad_l2)
GAMEPAD_R2: Final[int] = int(KeyFlags.gamepad_r2)
GAMEPAD_L3: Final[int] = int(KeyFlags.gamepad_l3)
GAMEPAD_R3: Final[int] = int(KeyFlags.gamepad_r3)
GAMEPAD_L_STICK_LEFT: Final[int] = int(KeyFlags.gamepad_l_stick_left)
GAMEPAD_L_STICK_RIGHT: Final[int] = int(KeyFlags.gamepad_l_stick_right)
GAMEPAD_L_STICK_UP: Final[int] = int(KeyFlags.gamepad_l_stick_up)
GAMEPAD_L_STICK_DOWN: Final[int] = int(KeyFlags.gamepad_l_stick_down)
GAMEPAD_R_STICK_LEFT: Final[int] = int(KeyFlags.gamepad_r_stick_left)
GAMEPAD_R_STICK_RIGHT: Final[int] = int(KeyFlags.gamepad_r_stick_right)
GAMEPAD_R_STICK_UP: Final[int] = int(KeyFlags.gamepad_r_stick_up)
GAMEPAD_R_STICK_DOWN: Final[int] = int(KeyFlags.gamepad_r_stick_down)
MOUSE_LEFT: Final[int] = int(KeyFlags.mouse_left)
MOUSE_RIGHT: Final[int] = int(KeyFlags.mouse_right)
MOUSE_MIDDLE: Final[int] = int(KeyFlags.mouse_middle)
MOUSE_X1: Final[int] = int(KeyFlags.mouse_x1)
MOUSE_X2: Final[int] = int(KeyFlags.mouse_x2)
MOUSE_WHEEL_X: Final[int] = int(KeyFlags.mouse_wheel_x)
MOUSE_WHEEL_Y: Final[int] = int(KeyFlags.mouse_wheel_y)
RESERVED_FOR_MOD_CTRL: Final[int] = int(KeyFlags.reserved_for_mod_ctrl)
RESERVED_FOR_MOD_SHIFT: Final[int] = int(KeyFlags.reserved_for_mod_shift)
RESERVED_FOR_MOD_ALT: Final[int] = int(KeyFlags.reserved_for_mod_alt)
RESERVED_FOR_MOD_SUPER: Final[int] = int(KeyFlags.reserved_for_mod_super)
NAMED_KEY_END: Final[int] = int(KeyFlags.named_key_end)
MOD_NONE: Final[int] = int(KeyFlags.mod_none)
MOD_CTRL: Final[int] = int(KeyFlags.mod_ctrl)
MOD_SHIFT: Final[int] = int(KeyFlags.mod_shift)
MOD_ALT: Final[int] = int(KeyFlags.mod_alt)
MOD_SUPER: Final[int] = int(KeyFlags.mod_super)
MOD_MASK_: Final[int] = int(KeyFlags.mod_mask_)


def merge_key_flags(*flags: Union[KeyFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))

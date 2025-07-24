# -*- coding: utf-8 -*-

from typing import Callable, Optional, Self

# noinspection PyPep8Naming
from cvp.imgui.flags.key import KeyFlags as _K
from cvp.imgui.flags.key import KeyLike
from cvp.imgui.widgets.shortcut import Shortcut


class ShortcutBuilder:
    def __init__(
        self,
        key: Optional[KeyLike] = None,
        shift: Optional[bool] = None,
        ctrl: Optional[bool] = None,
        alt: Optional[bool] = None,
        meta: Optional[bool] = None,
        repeat=False,
        label: Optional[str] = None,
        callback: Optional[Callable[[], None]] = None,
    ):
        self._key = key
        self._shift = shift
        self._ctrl = ctrl
        self._alt = alt
        self._meta = meta
        self._repeat = repeat
        self._label = label
        self._callback = callback

    def build(self) -> Shortcut:
        return Shortcut(
            key=self._key if self._key is not None else _K.none,
            shift=self._shift,
            ctrl=self._ctrl,
            alt=self._alt,
            meta=self._meta,
            repeat=self._repeat,
            label=self._label,
            callback=self._callback,
        )

    def __call__(self):
        return self.build()

    def set_callback(self, callback: Callable[[], None]) -> Self:
        self._callback = callback
        return self

    @property
    def shift(self) -> Self:
        self._shift = True
        return self

    @property
    def no_shift(self) -> Self:
        self._shift = False
        return self

    @property
    def none_shift(self) -> Self:
        self._shift = None
        return self

    @property
    def ctrl(self) -> Self:
        self._ctrl = True
        return self

    @property
    def no_ctrl(self) -> Self:
        self._ctrl = False
        return self

    @property
    def none_ctrl(self) -> Self:
        self._ctrl = None
        return self

    @property
    def alt(self) -> Self:
        self._alt = True
        return self

    @property
    def no_alt(self) -> Self:
        self._alt = False
        return self

    @property
    def none_alt(self) -> Self:
        self._alt = None
        return self

    @property
    def meta(self) -> Self:
        self._meta = True
        return self

    @property
    def no_meta(self) -> Self:
        self._meta = False
        return self

    @property
    def none_meta(self) -> Self:
        self._meta = None
        return self

    @property
    def only_shift(self) -> Self:
        self._shift = True
        self._ctrl = False
        self._alt = False
        self._meta = False
        return self

    @property
    def only_ctrl(self) -> Self:
        self._shift = False
        self._ctrl = True
        self._alt = False
        self._meta = False
        return self

    @property
    def only_alt(self) -> Self:
        self._shift = False
        self._ctrl = False
        self._alt = True
        self._meta = False
        return self

    @property
    def only_meta(self) -> Self:
        self._shift = False
        self._ctrl = False
        self._alt = False
        self._meta = True
        return self

    @property
    def only_shift_ctrl(self) -> Self:
        self._shift = True
        self._ctrl = True
        self._alt = False
        self._meta = False
        return self

    @property
    def only_ctrl_alt(self) -> Self:
        self._shift = False
        self._ctrl = True
        self._alt = True
        self._meta = False
        return self

    @property
    def only_shift_alt(self) -> Self:
        self._shift = True
        self._ctrl = False
        self._alt = True
        self._meta = False
        return self

    @property
    def only_shift_ctrl_alt(self) -> Self:
        self._shift = True
        self._ctrl = True
        self._alt = True
        self._meta = False
        return self

    @property
    def repeat(self) -> Self:
        self._repeat = True
        return self

    @property
    def no_repeat(self) -> Self:
        self._repeat = False
        return self

    def set_k(self, key: _K) -> Self:
        self._key = key
        return self

    tab = property(lambda self: self.set_k(_K.tab))
    left_arrow = property(lambda self: self.set_k(_K.left_arrow))
    right_arrow = property(lambda self: self.set_k(_K.right_arrow))
    up_arrow = property(lambda self: self.set_k(_K.up_arrow))
    down_arrow = property(lambda self: self.set_k(_K.down_arrow))
    page_up = property(lambda self: self.set_k(_K.page_up))
    page_down = property(lambda self: self.set_k(_K.page_down))
    home = property(lambda self: self.set_k(_K.home))
    end = property(lambda self: self.set_k(_K.end))
    insert = property(lambda self: self.set_k(_K.insert))
    delete = property(lambda self: self.set_k(_K.delete))
    backspace = property(lambda self: self.set_k(_K.backspace))
    space = property(lambda self: self.set_k(_K.space))
    enter = property(lambda self: self.set_k(_K.enter))
    escape = property(lambda self: self.set_k(_K.escape))
    menu = property(lambda self: self.set_k(_K.menu))

    n0 = property(lambda self: self.set_k(_K.n0))
    n1 = property(lambda self: self.set_k(_K.n1))
    n2 = property(lambda self: self.set_k(_K.n2))
    n3 = property(lambda self: self.set_k(_K.n3))
    n4 = property(lambda self: self.set_k(_K.n4))
    n5 = property(lambda self: self.set_k(_K.n5))
    n6 = property(lambda self: self.set_k(_K.n6))
    n7 = property(lambda self: self.set_k(_K.n7))
    n8 = property(lambda self: self.set_k(_K.n8))
    n9 = property(lambda self: self.set_k(_K.n9))

    a = property(lambda self: self.set_k(_K.a))
    b = property(lambda self: self.set_k(_K.b))
    c = property(lambda self: self.set_k(_K.c))
    d = property(lambda self: self.set_k(_K.d))
    e = property(lambda self: self.set_k(_K.e))
    f = property(lambda self: self.set_k(_K.f))
    g = property(lambda self: self.set_k(_K.g))
    h = property(lambda self: self.set_k(_K.h))
    i = property(lambda self: self.set_k(_K.i))
    j = property(lambda self: self.set_k(_K.j))
    k = property(lambda self: self.set_k(_K.k))
    l = property(lambda self: self.set_k(_K.l))  # noqa: E741
    m = property(lambda self: self.set_k(_K.m))
    n = property(lambda self: self.set_k(_K.n))
    o = property(lambda self: self.set_k(_K.o))
    p = property(lambda self: self.set_k(_K.p))
    q = property(lambda self: self.set_k(_K.q))
    r = property(lambda self: self.set_k(_K.r))
    s = property(lambda self: self.set_k(_K.s))
    t = property(lambda self: self.set_k(_K.t))
    u = property(lambda self: self.set_k(_K.u))
    v = property(lambda self: self.set_k(_K.v))
    w = property(lambda self: self.set_k(_K.w))
    x = property(lambda self: self.set_k(_K.x))
    y = property(lambda self: self.set_k(_K.y))
    z = property(lambda self: self.set_k(_K.z))

    f1 = property(lambda self: self.set_k(_K.f1))
    f2 = property(lambda self: self.set_k(_K.f2))
    f3 = property(lambda self: self.set_k(_K.f3))
    f4 = property(lambda self: self.set_k(_K.f4))
    f5 = property(lambda self: self.set_k(_K.f5))
    f6 = property(lambda self: self.set_k(_K.f6))
    f7 = property(lambda self: self.set_k(_K.f7))
    f8 = property(lambda self: self.set_k(_K.f8))
    f9 = property(lambda self: self.set_k(_K.f9))
    f10 = property(lambda self: self.set_k(_K.f10))
    f11 = property(lambda self: self.set_k(_K.f11))
    f12 = property(lambda self: self.set_k(_K.f12))
    f13 = property(lambda self: self.set_k(_K.f13))
    f14 = property(lambda self: self.set_k(_K.f14))
    f15 = property(lambda self: self.set_k(_K.f15))
    f16 = property(lambda self: self.set_k(_K.f16))
    f17 = property(lambda self: self.set_k(_K.f17))
    f18 = property(lambda self: self.set_k(_K.f18))
    f19 = property(lambda self: self.set_k(_K.f19))
    f20 = property(lambda self: self.set_k(_K.f20))
    f21 = property(lambda self: self.set_k(_K.f21))
    f22 = property(lambda self: self.set_k(_K.f22))
    f23 = property(lambda self: self.set_k(_K.f23))
    f24 = property(lambda self: self.set_k(_K.f24))

    apostrophe = property(lambda self: self.set_k(_K.apostrophe))
    comma = property(lambda self: self.set_k(_K.comma))
    minus = property(lambda self: self.set_k(_K.minus))
    period = property(lambda self: self.set_k(_K.period))
    slash = property(lambda self: self.set_k(_K.slash))
    semicolon = property(lambda self: self.set_k(_K.semicolon))
    equal = property(lambda self: self.set_k(_K.equal))
    left_bracket = property(lambda self: self.set_k(_K.left_bracket))
    backslash = property(lambda self: self.set_k(_K.backslash))
    right_bracket = property(lambda self: self.set_k(_K.right_bracket))
    grave_accent = property(lambda self: self.set_k(_K.grave_accent))
    caps_lock = property(lambda self: self.set_k(_K.caps_lock))
    scroll_lock = property(lambda self: self.set_k(_K.scroll_lock))
    num_lock = property(lambda self: self.set_k(_K.num_lock))
    print_screen = property(lambda self: self.set_k(_K.print_screen))
    pause = property(lambda self: self.set_k(_K.pause))

    keypad0 = property(lambda self: self.set_k(_K.keypad0))
    keypad1 = property(lambda self: self.set_k(_K.keypad1))
    keypad2 = property(lambda self: self.set_k(_K.keypad2))
    keypad3 = property(lambda self: self.set_k(_K.keypad3))
    keypad4 = property(lambda self: self.set_k(_K.keypad4))
    keypad5 = property(lambda self: self.set_k(_K.keypad5))
    keypad6 = property(lambda self: self.set_k(_K.keypad6))
    keypad7 = property(lambda self: self.set_k(_K.keypad7))
    keypad8 = property(lambda self: self.set_k(_K.keypad8))
    keypad9 = property(lambda self: self.set_k(_K.keypad9))
    keypad_decimal = property(lambda self: self.set_k(_K.keypad_decimal))
    keypad_divide = property(lambda self: self.set_k(_K.keypad_divide))
    keypad_multiply = property(lambda self: self.set_k(_K.keypad_multiply))
    keypad_subtract = property(lambda self: self.set_k(_K.keypad_subtract))
    keypad_add = property(lambda self: self.set_k(_K.keypad_add))
    keypad_enter = property(lambda self: self.set_k(_K.keypad_enter))
    keypad_equal = property(lambda self: self.set_k(_K.keypad_equal))

    app_back = property(lambda self: self.set_k(_K.app_back))
    app_forward = property(lambda self: self.set_k(_K.app_forward))

    gamepad_start = property(lambda self: self.set_k(_K.gamepad_start))
    gamepad_back = property(lambda self: self.set_k(_K.gamepad_back))
    gamepad_face_left = property(lambda self: self.set_k(_K.gamepad_face_left))
    gamepad_face_right = property(lambda self: self.set_k(_K.gamepad_face_right))
    gamepad_face_up = property(lambda self: self.set_k(_K.gamepad_face_up))
    gamepad_face_down = property(lambda self: self.set_k(_K.gamepad_face_down))
    gamepad_dpad_left = property(lambda self: self.set_k(_K.gamepad_dpad_left))
    gamepad_dpad_right = property(lambda self: self.set_k(_K.gamepad_dpad_right))
    gamepad_dpad_up = property(lambda self: self.set_k(_K.gamepad_dpad_up))
    gamepad_dpad_down = property(lambda self: self.set_k(_K.gamepad_dpad_down))
    gamepad_l1 = property(lambda self: self.set_k(_K.gamepad_l1))
    gamepad_r1 = property(lambda self: self.set_k(_K.gamepad_r1))
    gamepad_l2 = property(lambda self: self.set_k(_K.gamepad_l2))
    gamepad_r2 = property(lambda self: self.set_k(_K.gamepad_r2))
    gamepad_l3 = property(lambda self: self.set_k(_K.gamepad_l3))
    gamepad_r3 = property(lambda self: self.set_k(_K.gamepad_r3))
    gamepad_l_stick_left = property(lambda self: self.set_k(_K.gamepad_l_stick_left))
    gamepad_l_stick_right = property(lambda self: self.set_k(_K.gamepad_l_stick_right))
    gamepad_l_stick_up = property(lambda self: self.set_k(_K.gamepad_l_stick_up))
    gamepad_l_stick_down = property(lambda self: self.set_k(_K.gamepad_l_stick_down))
    gamepad_r_stick_left = property(lambda self: self.set_k(_K.gamepad_r_stick_left))
    gamepad_r_stick_right = property(lambda self: self.set_k(_K.gamepad_r_stick_right))
    gamepad_r_stick_up = property(lambda self: self.set_k(_K.gamepad_r_stick_up))
    gamepad_r_stick_down = property(lambda self: self.set_k(_K.gamepad_r_stick_down))

    mouse_left = property(lambda self: self.set_k(_K.mouse_left))
    mouse_right = property(lambda self: self.set_k(_K.mouse_right))
    mouse_middle = property(lambda self: self.set_k(_K.mouse_middle))
    mouse_x1 = property(lambda self: self.set_k(_K.mouse_x1))
    mouse_x2 = property(lambda self: self.set_k(_K.mouse_x2))
    mouse_wheel_x = property(lambda self: self.set_k(_K.mouse_wheel_x))
    mouse_wheel_y = property(lambda self: self.set_k(_K.mouse_wheel_y))

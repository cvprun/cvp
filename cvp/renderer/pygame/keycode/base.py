# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import pygame

from cvp.types.override import override


class KeycodeRemapperInterface(ABC):
    @abstractmethod
    def _at(self, pygame_keycode: int) -> int:
        raise NotImplementedError


class BaseKeycodeRemapper(KeycodeRemapperInterface):
    def __init__(self):
        self.null = self._at(0)

        self.num_0 = self._at(pygame.K_0)
        self.num_1 = self._at(pygame.K_1)
        self.num_2 = self._at(pygame.K_2)
        self.num_3 = self._at(pygame.K_3)
        self.num_4 = self._at(pygame.K_4)
        self.num_5 = self._at(pygame.K_5)
        self.num_6 = self._at(pygame.K_6)
        self.num_7 = self._at(pygame.K_7)
        self.num_8 = self._at(pygame.K_8)
        self.num_9 = self._at(pygame.K_9)

        self.a = self._at(pygame.K_a)
        self.b = self._at(pygame.K_b)
        self.c = self._at(pygame.K_c)
        self.d = self._at(pygame.K_d)
        self.e = self._at(pygame.K_e)
        self.f = self._at(pygame.K_f)
        self.g = self._at(pygame.K_g)
        self.h = self._at(pygame.K_h)
        self.i = self._at(pygame.K_i)
        self.j = self._at(pygame.K_j)
        self.k = self._at(pygame.K_k)
        self.l = self._at(pygame.K_l)  # noqa: E741
        self.m = self._at(pygame.K_m)
        self.n = self._at(pygame.K_n)
        self.o = self._at(pygame.K_o)
        self.p = self._at(pygame.K_p)
        self.q = self._at(pygame.K_q)
        self.r = self._at(pygame.K_r)
        self.s = self._at(pygame.K_s)
        self.t = self._at(pygame.K_t)
        self.u = self._at(pygame.K_u)
        self.v = self._at(pygame.K_v)
        self.w = self._at(pygame.K_w)
        self.x = self._at(pygame.K_x)
        self.y = self._at(pygame.K_y)
        self.z = self._at(pygame.K_z)

        self.tab = self._at(pygame.K_TAB)
        self.left_arrow = self._at(pygame.K_LEFT)
        self.right_arrow = self._at(pygame.K_RIGHT)
        self.up_arrow = self._at(pygame.K_UP)
        self.down_arrow = self._at(pygame.K_DOWN)
        self.page_up = self._at(pygame.K_PAGEUP)
        self.page_down = self._at(pygame.K_PAGEDOWN)
        self.home = self._at(pygame.K_HOME)
        self.end = self._at(pygame.K_END)
        self.insert = self._at(pygame.K_INSERT)
        self.delete = self._at(pygame.K_DELETE)
        self.backspace = self._at(pygame.K_BACKSPACE)
        self.space = self._at(pygame.K_SPACE)
        self.enter = self._at(pygame.K_RETURN)
        self.escape = self._at(pygame.K_ESCAPE)

        self.l_ctrl = self._at(pygame.K_LCTRL)
        self.r_ctrl = self._at(pygame.K_RCTRL)
        self.l_alt = self._at(pygame.K_LALT)
        self.r_alt = self._at(pygame.K_RALT)
        self.l_shift = self._at(pygame.K_LSHIFT)
        self.r_shift = self._at(pygame.K_RSHIFT)
        self.l_super = self._at(pygame.K_LSUPER)
        self.r_super = self._at(pygame.K_RSUPER)

        self.keypad_0 = self._at(pygame.K_KP_0)
        self.keypad_1 = self._at(pygame.K_KP_1)
        self.keypad_2 = self._at(pygame.K_KP_2)
        self.keypad_3 = self._at(pygame.K_KP_3)
        self.keypad_4 = self._at(pygame.K_KP_4)
        self.keypad_5 = self._at(pygame.K_KP_5)
        self.keypad_6 = self._at(pygame.K_KP_6)
        self.keypad_7 = self._at(pygame.K_KP_7)
        self.keypad_8 = self._at(pygame.K_KP_8)
        self.keypad_9 = self._at(pygame.K_KP_9)
        self.keypad_divide = self._at(pygame.K_KP_DIVIDE)
        self.keypad_enter = self._at(pygame.K_KP_ENTER)
        self.keypad_equals = self._at(pygame.K_KP_EQUALS)
        self.keypad_minus = self._at(pygame.K_KP_MINUS)
        self.keypad_multiply = self._at(pygame.K_KP_MULTIPLY)
        self.keypad_period = self._at(pygame.K_KP_PERIOD)
        self.keypad_plus = self._at(pygame.K_KP_PLUS)

        self.f1 = self._at(pygame.K_F1)
        self.f2 = self._at(pygame.K_F2)
        self.f3 = self._at(pygame.K_F3)
        self.f4 = self._at(pygame.K_F4)
        self.f5 = self._at(pygame.K_F5)
        self.f6 = self._at(pygame.K_F6)
        self.f7 = self._at(pygame.K_F7)
        self.f8 = self._at(pygame.K_F8)
        self.f9 = self._at(pygame.K_F9)
        self.f10 = self._at(pygame.K_F10)
        self.f11 = self._at(pygame.K_F11)
        self.f12 = self._at(pygame.K_F12)
        self.f13 = self._at(pygame.K_F13)
        self.f14 = self._at(pygame.K_F14)
        self.f15 = self._at(pygame.K_F15)

    @override
    def _at(self, pygame_keycode: int) -> int:
        raise NotImplementedError

    def __call__(self, pygame_keycode: int) -> int:
        return self._at(pygame_keycode)

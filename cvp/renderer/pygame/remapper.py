# -*- coding: utf-8 -*-

from typing import Dict, Final

import pygame

ASCII_RANGE: Final[int] = 127
MAX_IMGUI_KEYCODE: Final[int] = 512


class KeycodeRemapper:
    """
    We need to go to custom keycode since imgui only support keycode from 0..512 or -1
    """

    _pygame_to_imgui: Dict[int, int]

    def __init__(self):
        self._pygame_to_imgui = dict()

        # Maps so that accesses like `imgui.is_key_pressed(ord("a"))` are equivalent.
        for i in range(ASCII_RANGE):
            self._pygame_to_imgui[i] = i

        # In pygame, keymaps are not case-sensitive.
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self._pygame_to_imgui[ord(c)] = ord(c.lower())

        assert 33 == self._at(ord("!"))
        assert 34 == self._at(ord('"'))
        assert 35 == self._at(ord("#"))
        assert 36 == self._at(ord("$"))
        assert 37 == self._at(ord("%"))
        assert 38 == self._at(ord("&"))
        assert 39 == self._at(ord("'"))
        assert 40 == self._at(ord("("))
        assert 41 == self._at(ord(")"))
        assert 42 == self._at(ord("*"))
        assert 43 == self._at(ord("+"))
        assert 44 == self._at(ord(","))
        assert 45 == self._at(ord("-"))
        assert 46 == self._at(ord("."))
        assert 47 == self._at(ord("/"))

        assert 48 == self._at(ord("0"))
        assert 49 == self._at(ord("1"))
        assert 50 == self._at(ord("2"))
        assert 51 == self._at(ord("3"))
        assert 52 == self._at(ord("4"))
        assert 53 == self._at(ord("5"))
        assert 54 == self._at(ord("6"))
        assert 55 == self._at(ord("7"))
        assert 56 == self._at(ord("8"))
        assert 57 == self._at(ord("9"))

        assert 58 == self._at(ord(":"))
        assert 59 == self._at(ord(";"))
        assert 60 == self._at(ord("<"))
        assert 61 == self._at(ord("="))
        assert 62 == self._at(ord(">"))
        assert 63 == self._at(ord("?"))
        assert 64 == self._at(ord("@"))

        assert 97 == self._at(ord("A"))
        assert 98 == self._at(ord("B"))
        assert 99 == self._at(ord("C"))
        assert 100 == self._at(ord("D"))
        assert 101 == self._at(ord("E"))
        assert 102 == self._at(ord("F"))
        assert 103 == self._at(ord("G"))
        assert 104 == self._at(ord("H"))
        assert 105 == self._at(ord("I"))
        assert 106 == self._at(ord("J"))
        assert 107 == self._at(ord("K"))
        assert 108 == self._at(ord("L"))
        assert 109 == self._at(ord("M"))
        assert 110 == self._at(ord("N"))
        assert 111 == self._at(ord("O"))
        assert 112 == self._at(ord("P"))
        assert 113 == self._at(ord("Q"))
        assert 114 == self._at(ord("R"))
        assert 115 == self._at(ord("S"))
        assert 116 == self._at(ord("T"))
        assert 117 == self._at(ord("U"))
        assert 118 == self._at(ord("V"))
        assert 119 == self._at(ord("W"))
        assert 120 == self._at(ord("X"))
        assert 121 == self._at(ord("Y"))
        assert 122 == self._at(ord("Z"))

        assert 91 == self._at(ord("["))
        assert 92 == self._at(ord("\\"))
        assert 93 == self._at(ord("]"))
        assert 94 == self._at(ord("^"))
        assert 95 == self._at(ord("_"))
        assert 96 == self._at(ord("`"))

        assert 97 == self._at(ord("a"))
        assert 98 == self._at(ord("b"))
        assert 99 == self._at(ord("c"))
        assert 100 == self._at(ord("d"))
        assert 101 == self._at(ord("e"))
        assert 102 == self._at(ord("f"))
        assert 103 == self._at(ord("g"))
        assert 104 == self._at(ord("h"))
        assert 105 == self._at(ord("i"))
        assert 106 == self._at(ord("j"))
        assert 107 == self._at(ord("k"))
        assert 108 == self._at(ord("l"))
        assert 109 == self._at(ord("m"))
        assert 110 == self._at(ord("n"))
        assert 111 == self._at(ord("o"))
        assert 112 == self._at(ord("p"))
        assert 113 == self._at(ord("q"))
        assert 114 == self._at(ord("r"))
        assert 115 == self._at(ord("s"))
        assert 116 == self._at(ord("t"))
        assert 117 == self._at(ord("u"))
        assert 118 == self._at(ord("v"))
        assert 119 == self._at(ord("w"))
        assert 120 == self._at(ord("x"))
        assert 121 == self._at(ord("y"))
        assert 122 == self._at(ord("z"))

        assert 123 == self._at(ord("{"))
        assert 124 == self._at(ord("|"))
        assert 125 == self._at(ord("}"))
        assert 126 == self._at(ord("~"))

        self.null = self._at(0)

        assert 0 == self.null

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

        assert 48 == self.num_0
        assert 49 == self.num_1
        assert 50 == self.num_2
        assert 51 == self.num_3
        assert 52 == self.num_4
        assert 53 == self.num_5
        assert 54 == self.num_6
        assert 55 == self.num_7
        assert 56 == self.num_8
        assert 57 == self.num_9

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

        assert 97 == self.a
        assert 98 == self.b
        assert 99 == self.c
        assert 100 == self.d
        assert 101 == self.e
        assert 102 == self.f
        assert 103 == self.g
        assert 104 == self.h
        assert 105 == self.i
        assert 106 == self.j
        assert 107 == self.k
        assert 108 == self.l
        assert 109 == self.m
        assert 110 == self.n
        assert 111 == self.o
        assert 112 == self.p
        assert 113 == self.q
        assert 114 == self.r
        assert 115 == self.s
        assert 116 == self.t
        assert 117 == self.u
        assert 118 == self.v
        assert 119 == self.w
        assert 120 == self.x
        assert 121 == self.y
        assert 122 == self.z

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
        self.pad_enter = self._at(pygame.K_KP_ENTER)

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

    def get_next_index(self) -> int:
        i = len(self._pygame_to_imgui)

        while i in self._pygame_to_imgui:
            i += 1

        if MAX_IMGUI_KEYCODE < i:
            raise ValueError("The keymap has exceeded the maximum limit")

        assert i not in self._pygame_to_imgui
        return i

    def _at(self, pygame_keycode: int) -> int:
        if pygame_keycode in self._pygame_to_imgui:
            return self._pygame_to_imgui[pygame_keycode]
        else:
            next_index = self.get_next_index()
            self._pygame_to_imgui[pygame_keycode] = next_index
            return next_index

    def __call__(self, pygame_keycode: int) -> int:
        return self._at(pygame_keycode)

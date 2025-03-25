# -*- coding: utf-8 -*-

from typing import Dict

from cvp.renderer.pygame.keycode.base import BaseKeycodeRemapper
from cvp.types.override import override
from cvp.variables import ASCII_RANGE, MAX_IMGUI_KEYCODE


class PyimguiKeycodeRemapper(BaseKeycodeRemapper):
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

        assert 0 == self._at(0)

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

        super().__init__()

    def _get_next_index(self) -> int:
        i = len(self._pygame_to_imgui)

        while i in self._pygame_to_imgui:
            i += 1

        if MAX_IMGUI_KEYCODE < i:
            raise ValueError("The keymap has exceeded the maximum limit")

        assert i not in self._pygame_to_imgui
        return i

    @override
    def _at(self, pygame_keycode: int) -> int:
        if pygame_keycode in self._pygame_to_imgui:
            return self._pygame_to_imgui[pygame_keycode]
        else:
            next_index = self._get_next_index()
            self._pygame_to_imgui[pygame_keycode] = next_index
            return next_index

# -*- coding: utf-8 -*-

from cvp.ime.sources._base import BaseInputHandler


class EnglishInputHandler(BaseInputHandler):
    __cvp_ime_method_name__ = "english"
    __cvp_ime_keyboard_layout__ = "qwerty"
    __cvp_ime_language__ = "english"

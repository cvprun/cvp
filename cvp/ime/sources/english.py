# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.ime.sources._base import BaseInputHandler
from cvp.types.override import override


class EnglishInputHandler(BaseInputHandler):
    __cvp_ime_method_name__ = "english"
    __cvp_ime_keyboard_layout__ = "qwerty"
    __cvp_ime_language__ = "english"

    @override
    def add(self, text: str) -> Sequence[str]:
        return (text,)

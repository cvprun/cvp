# -*- coding: utf-8 -*-

from typing import Optional, Sequence

import hgtk

from cvp.ime.sources._base import BaseInputHandler
from cvp.types.override import override


def create_dubeolsik_hangul_mapping():
    return {
        "q": "ㅂ",
        "w": "ㅈ",
        "e": "ㄷ",
        "r": "ㄱ",
        "t": "ㅅ",
        "y": "ㅛ",
        "u": "ㅕ",
        "i": "ㅑ",
        "o": "ㅐ",
        "p": "ㅔ",
        "a": "ㅁ",
        "s": "ㄴ",
        "d": "ㅇ",
        "f": "ㄹ",
        "g": "ㅎ",
        "h": "ㅗ",
        "j": "ㅓ",
        "k": "ㅏ",
        "l": "ㅣ",
        "z": "ㅋ",
        "x": "ㅌ",
        "c": "ㅊ",
        "v": "ㅍ",
        "b": "ㅠ",
        "n": "ㅜ",
        "m": "ㅡ",
        "Q": "ㅃ",
        "W": "ㅉ",
        "E": "ㄸ",
        "R": "ㄲ",
        "T": "ㅆ",
        "Y": "ㅛ",
        "U": "ㅕ",
        "I": "ㅑ",
        "O": "ㅒ",
        "P": "ㅖ",
        "A": "ㅁ",
        "S": "ㄴ",
        "D": "ㅇ",
        "F": "ㄹ",
        "G": "ㅎ",
        "H": "ㅗ",
        "J": "ㅓ",
        "K": "ㅏ",
        "L": "ㅣ",
        "Z": "ㅋ",
        "X": "ㅌ",
        "C": "ㅊ",
        "V": "ㅍ",
        "B": "ㅠ",
        "N": "ㅜ",
        "M": "ㅡ",
    }


class DubeolsikHangulInputHandler(BaseInputHandler):
    """
    https://en.wikipedia.org/wiki/Keyboard_layout#Dubeolsik
    """

    __cvp_ime_method_name__ = "hangul"
    __cvp_ime_keyboard_layout__ = "dubeolsik"  # QWERTY
    __cvp_ime_language__ = "korean"

    def __init__(
        self,
        *,
        composing: Optional[str] = None,
    ):
        super().__init__()
        self._composing = composing if composing else str()
        self._keyboard_mapping = create_dubeolsik_hangul_mapping()

    @staticmethod
    def compose(text: str, compose_code=hgtk.text.DEFAULT_COMPOSE_CODE) -> str:
        return hgtk.text.compose(text, compose_code=compose_code)

    @staticmethod
    def decompose(text: str, compose_code=hgtk.text.DEFAULT_COMPOSE_CODE) -> str:
        return hgtk.text.decompose(text, compose_code=compose_code)

    @override
    def get_composing(self) -> str:
        return self._composing

    @override
    def add(self, text: str) -> Sequence[str]:
        if 1 != len(text):
            raise ValueError("Only one character must be added")

        hangul_text = self._keyboard_mapping.get(text, text)
        assert 1 == len(hangul_text)

        if not hgtk.checker.is_hangul(hangul_text):
            if self._composing:
                emit_result = self._composing, hangul_text
                self._composing = str()
                return emit_result
            else:
                return (hangul_text,)

        if not self._composing:
            self._composing = hangul_text
            return (str(),)

        # TODO: ERROR!!
        composed_hangul_text = hgtk.text.compose(self._composing + hangul_text)

        match len(composed_hangul_text):
            case 1:
                self._composing = composed_hangul_text
                return (str(),)
            case 2:
                emit_text = composed_hangul_text[0]
                remain_text = composed_hangul_text[1]
                if hgtk.checker.is_hangul(remain_text):
                    self._composing = remain_text
                    return (emit_text,)
                else:
                    self._composing = str()
                    return emit_text, remain_text
            case _:
                assert False, "Inaccessible section"

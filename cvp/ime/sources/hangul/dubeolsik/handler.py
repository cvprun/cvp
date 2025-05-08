# -*- coding: utf-8 -*-

from typing import Sequence

import hgtk
from overrides import override

from cvp.ime.sources._base import BaseInputHandler
from cvp.ime.sources.hangul.dubeolsik.mapping import create_dubeolsik_hangul_mapping
from cvp.ime.sources.hangul.dubeolsik.syllables import HangulSyllables
from cvp.unicode.hangul.compatibility_jamo import is_hangul_compatibility_jamo_unicode


class DubeolsikHangulInputHandler(BaseInputHandler):
    """
    https://en.wikipedia.org/wiki/Keyboard_layout#Dubeolsik
    """

    __cvp_ime_method_name__ = "hangul"
    __cvp_ime_keyboard_layout__ = "dubeolsik"  # QWERTY
    __cvp_ime_language__ = "korean"

    def __init__(self):
        super().__init__()
        self._composing = str()
        self._syllables = HangulSyllables()
        self._keyboard_mapping = create_dubeolsik_hangul_mapping()

    @override
    def has_composing(self) -> bool:
        return self._syllables.__bool__()

    @override
    def get_composing(self) -> str:
        return self._syllables.compose()

    @override
    def del_composing(self) -> None:
        self._syllables.pop()

    @override
    def clear_composing(self) -> None:
        self._syllables.clear()

    @override
    def add(self, text: str) -> Sequence[str]:
        if 1 != len(text):
            raise ValueError("Only one character must be added")

        hangul_char = self._keyboard_mapping.get(text, text)
        assert 1 == len(hangul_char)

        if not is_hangul_compatibility_jamo_unicode(hangul_char):
            if self.has_composing():
                return self.pop_composing(), hangul_char
            else:
                return (hangul_char,)

        if not self.has_composing():
            # TODO: check cho, jung, jong
            # self._syllables.push(hangul_char)
            return ()

        # TODO: ERROR!!
        composed_hangul_text = hgtk.text.compose(self._composing + hangul_char)

        match len(composed_hangul_text):
            case 1:
                self._composing = composed_hangul_text
                return ()
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

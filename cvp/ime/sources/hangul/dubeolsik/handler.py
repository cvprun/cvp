# -*- coding: utf-8 -*-

from typing import Sequence

from overrides import override

from cvp.ime.sources._base import BaseInputHandler
from cvp.ime.sources.hangul.dubeolsik.complexing import (
    create_consonants_complexing,
    create_vowels_complexing,
)
from cvp.ime.sources.hangul.dubeolsik.components import HangulComponents
from cvp.ime.sources.hangul.dubeolsik.mapping import (
    DUBEOLSIK_CONSONANTS,
    DUBEOLSIK_JAMOS,
    DUBEOLSIK_VOWELS,
    create_dubeolsik_hangul_mapping,
)
from cvp.unicode.hangul.compatibility_jamo import MODERN_JONGSEONG_AS_CHOSEONG_SET


class DubeolsikHangulInputHandler(BaseInputHandler):
    """
    https://en.wikipedia.org/wiki/Keyboard_layout#Dubeolsik
    """

    __cvp_ime_method_name__ = "hangul"
    __cvp_ime_keyboard_layout__ = "dubeolsik"  # QWERTY
    __cvp_ime_language__ = "korean"

    KEYBOARD_MAPPING = create_dubeolsik_hangul_mapping()
    CONSONANTS_COMPLEXING = create_consonants_complexing()
    VOWELS_COMPLEXING = create_vowels_complexing()

    def __init__(self):
        super().__init__()
        self._composing = str()
        self._syllables = HangulComponents()

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

        hangul_char = self.KEYBOARD_MAPPING.get(text, text)
        assert 1 == len(hangul_char)

        if hangul_char not in DUBEOLSIK_JAMOS:
            if self.has_composing():
                return self.pop_composing(), hangul_char
            else:
                return (hangul_char,)

        is_consonants = hangul_char in DUBEOLSIK_CONSONANTS
        is_vowels = hangul_char in DUBEOLSIK_VOWELS
        assert is_consonants != is_vowels

        match self._syllables:
            case (None, None, None):
                if is_consonants:
                    self._syllables.choseong = hangul_char
                    return ()
                else:
                    assert is_vowels
                    return (hangul_char,)
            case (cho, None, None) if cho:
                if is_consonants:
                    if complexing := self.CONSONANTS_COMPLEXING.get(cho):
                        if jongseong := complexing.get(hangul_char):
                            pass
                    self._syllables.choseong = hangul_char
                    return (cho,)
                else:
                    assert is_vowels
                    self._syllables.jungseong = hangul_char
                    return ()
            case (cho, jung, None) if cho and jung:
                if is_consonants:
                    if hangul_char in MODERN_JONGSEONG_AS_CHOSEONG_SET:
                        self._syllables.jongseong = hangul_char
                        return ()
                    else:
                        result = self.pop_composing()
                        self._syllables.choseong = hangul_char
                        return (result,)
                else:
                    assert is_vowels
                    pass
            case (cho, jung, jong) if cho and jung and jong:
                if is_consonants:
                    pass
                else:
                    assert is_vowels
                    pass
            case _:
                assert False, "Inaccessible section"

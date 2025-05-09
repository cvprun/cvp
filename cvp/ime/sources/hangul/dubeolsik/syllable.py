# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.ime.sources.hangul.dubeolsik.complexing import (
    create_jongseong_complex_mapping,
    create_jongseong_split_mapping,
    create_vowels_complex_mapping,
    create_vowels_split_mapping,
)
from cvp.ime.sources.hangul.dubeolsik.mapping import (
    DUBEOLSIK_CONSONANTS,
    DUBEOLSIK_JAMOS,
    DUBEOLSIK_VOWELS,
)
from cvp.unicode.hangul.combinator import compose_hangul_syllable
from cvp.unicode.hangul.compatibility_jamo import MODERN_JONGSEONG_AS_CHOSEONG_SET

JONGSEONG_COMPLEX_MAP = create_jongseong_complex_mapping()
JONGSEONG_SPLIT_MAP = create_jongseong_split_mapping()

VOWELS_COMPLEX_MAP = create_vowels_complex_mapping()
VOWELS_SPLIT_MAP = create_vowels_split_mapping()


class DubeolsikHangulSyllable:
    def __init__(
        self,
        choseong: Optional[str] = None,
        jungseong: Optional[str] = None,
        jongseong: Optional[str] = None,
    ):
        self.choseong = choseong
        self.jungseong = jungseong
        self.jongseong = jongseong

    def __bool__(self):
        return bool(self.any)

    def __iter__(self):
        yield self.choseong
        yield self.jungseong
        yield self.jongseong

    def clear(self):
        self.choseong = None
        self.jungseong = None
        self.jongseong = None

    @property
    def is_empty(self):
        return not self.choseong and not self.jungseong and not self.jongseong

    @property
    def any(self):
        return self.choseong or self.jungseong or self.jongseong

    @property
    def only_choseong(self):
        return not self.jungseong and not self.jongseong and self.choseong

    @property
    def only_jungseong(self):
        return not self.choseong and not self.jongseong and self.jungseong

    @property
    def only_jongseong(self):
        return not self.choseong and not self.jungseong and self.jongseong

    def compose(self) -> str:
        if self.is_empty:
            return str()

        if self.only_choseong:
            assert self.choseong
            return self.choseong

        if self.only_jungseong:
            assert self.jungseong
            return self.jungseong

        if self.only_jongseong:
            assert self.jongseong
            return self.jongseong

        if not self.choseong and self.jungseong and self.jongseong:
            assert False, "Inaccessible section"

        assert self.choseong and self.jungseong
        return compose_hangul_syllable(self.choseong, self.jungseong, self.jongseong)

    def compose_and_clear(
        self,
        *,
        choseong: Optional[str] = None,
        jungseong: Optional[str] = None,
        jongseong: Optional[str] = None,
    ) -> str:
        try:
            return self.compose()
        finally:
            self.clear()
            self.choseong = choseong
            self.jungseong = jungseong
            self.jongseong = jongseong

    def pop(self) -> Optional[str]:
        match (self.choseong, self.jungseong, self.jongseong):
            # --------------------------------------------------------------------------
            case (None, None, None):
                return None

            # --------------------------------------------------------------------------
            case (cho, None, None) if cho:
                self.choseong = None
                return cho

            # --------------------------------------------------------------------------
            case (None, jung, None) if jung:
                if split_jungseong := VOWELS_SPLIT_MAP.get(jung):
                    old_jung, new_jung = split_jungseong
                    self.jungseong = old_jung
                    return new_jung
                else:
                    self.jungseong = None
                    return jung

            # --------------------------------------------------------------------------
            case (None, None, jong) if jong:
                old_cho, new_cho = JONGSEONG_SPLIT_MAP[jong]
                self.choseong = old_cho
                self.jongseong = None
                return new_cho

            # --------------------------------------------------------------------------
            case (cho, jung, None) if cho and jung:
                if split_jungseong := VOWELS_SPLIT_MAP.get(jung):
                    old_jung, new_jung = split_jungseong
                    self.jungseong = old_jung
                    return new_jung
                else:
                    self.jungseong = None
                    return jung

            # --------------------------------------------------------------------------
            case (cho, jung, jong) if cho and jung and jong:
                if split_jongseong := JONGSEONG_SPLIT_MAP.get(jong):
                    old_jong, new_jong = split_jongseong
                    self.jongseong = old_jong
                    return new_jong
                else:
                    self.jongseong = None
                    return jong

            # --------------------------------------------------------------------------
            case _:
                assert False, "Inaccessible section"

    def push(self, text: str) -> Sequence[str]:
        if 1 != len(text):
            raise ValueError("Only one character must be added")

        if text == "\b":
            raise ValueError("Backspace is not allowed")

        if text not in DUBEOLSIK_JAMOS:
            if self.any:
                return self.compose_and_clear(), text
            else:
                return (text,)

        is_consonants = text in DUBEOLSIK_CONSONANTS
        is_vowels = text in DUBEOLSIK_VOWELS
        assert is_consonants != is_vowels

        match (self.choseong, self.jungseong, self.jongseong, is_consonants):
            # --------------------------------------------------------------------------
            case (None, None, None, True):
                self.choseong = text
                return ()

            # --------------------------------------------------------------------------
            case (None, None, None, False):
                self.jungseong = text
                return ()

            # --------------------------------------------------------------------------
            case (cho, None, None, True) if cho:
                if complexing := JONGSEONG_COMPLEX_MAP.get(cho):
                    if jongseong := complexing.get(text):
                        self.choseong = None
                        self.jongseong = jongseong
                        return ()
                self.choseong = text
                return (cho,)

            # --------------------------------------------------------------------------
            case (cho, None, None, False) if cho:
                self.jungseong = text
                return ()

            # --------------------------------------------------------------------------
            case (None, jung, None, True) if jung:
                return (self.compose_and_clear(choseong=text),)

            # --------------------------------------------------------------------------
            case (None, jung, None, False) if jung:
                if complexing := VOWELS_COMPLEX_MAP.get(jung):
                    if jungseong := complexing.get(text):
                        self.jungseong = jungseong
                        return ()
                self.jungseong = text
                return (jung,)

            # --------------------------------------------------------------------------
            case (None, None, jong, True) if jong:
                return (self.compose_and_clear(choseong=text),)

            # --------------------------------------------------------------------------
            case (None, None, jong, False) if jong:
                old_cho, new_cho = JONGSEONG_SPLIT_MAP[jong]
                self.clear()
                self.choseong = new_cho
                self.jungseong = text
                return (old_cho,)

            # --------------------------------------------------------------------------
            case (cho, jung, None, True) if cho and jung:
                if text in MODERN_JONGSEONG_AS_CHOSEONG_SET:
                    self.jongseong = text
                    return ()
                else:
                    return (self.compose_and_clear(choseong=text),)

            # --------------------------------------------------------------------------
            case (cho, jung, None, False) if cho and jung:
                if complexing := VOWELS_COMPLEX_MAP.get(jung):
                    if jungseong := complexing.get(text):
                        self.jungseong = jungseong
                        return ()
                return (self.compose_and_clear(jungseong=text),)

            # --------------------------------------------------------------------------
            case (cho, jung, jong, True) if cho and jung and jong:
                if complexing := JONGSEONG_COMPLEX_MAP.get(jong):
                    if jongseong := complexing.get(text):
                        self.jongseong = jongseong
                        return ()
                return (self.compose_and_clear(choseong=text),)

            # --------------------------------------------------------------------------
            case (cho, jung, jong, False) if cho and jung and jong:
                if split_jongseong := JONGSEONG_SPLIT_MAP.get(jong):
                    old_jong, new_cho = split_jongseong
                    self.jongseong = old_jong
                    return (self.compose_and_clear(choseong=new_cho, jungseong=text),)
                else:
                    self.jongseong = None
                    return (self.compose_and_clear(choseong=jong, jungseong=text),)

            # --------------------------------------------------------------------------
            case _:
                assert False, "Inaccessible section"

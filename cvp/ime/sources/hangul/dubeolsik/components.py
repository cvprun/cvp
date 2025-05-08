# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.unicode.hangul.combinator import compose_hangul_syllable


@dataclass
class HangulComponents:
    choseong: Optional[str] = None
    jungseong: Optional[str] = None
    jongseong: Optional[str] = None

    def __bool__(self):
        return bool(self.choseong) or bool(self.jungseong) or bool(self.jongseong)

    def __iter__(self):
        yield self.choseong
        yield self.jungseong
        yield self.jongseong

    def clear(self):
        self.choseong = None
        self.jungseong = None
        self.jongseong = None

    def compose(self) -> str:
        if not self.choseong:
            return str()

        if not self.jungseong:
            return self.choseong

        return compose_hangul_syllable(self.choseong, self.choseong, self.jongseong)

    def pop(self) -> Optional[str]:
        if self.jongseong:
            del_jongseong = self.jongseong
            self.jongseong = None
            return del_jongseong

        if self.jungseong:
            del_jungseong = self.jungseong
            self.jungseong = None
            return del_jungseong

        if self.choseong:
            del_choseong = self.choseong
            self.choseong = None
            return del_choseong

        return None

    def push(self, text: str) -> None:
        pass

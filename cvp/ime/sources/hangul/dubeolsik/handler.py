# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from overrides import override

from cvp.ime.sources._base import BaseInputHandler
from cvp.ime.sources.hangul.dubeolsik.mapping import create_dubeolsik_hangul_mapping
from cvp.ime.sources.hangul.dubeolsik.syllable import DubeolsikHangulSyllable


class DubeolsikHangulInputHandler(BaseInputHandler):
    """
    https://en.wikipedia.org/wiki/Keyboard_layout#Dubeolsik
    """

    __cvp_ime_method_name__ = "hangul"
    __cvp_ime_keyboard_layout__ = "dubeolsik"  # QWERTY
    __cvp_ime_language__ = "korean"

    def __init__(self):
        super().__init__()
        self._syllable = DubeolsikHangulSyllable()
        self._dubeolsik_hangul_map = create_dubeolsik_hangul_mapping()

    @override
    def has_composing(self) -> bool:
        return self._syllable.any

    @override
    def get_composing(self) -> str:
        return self._syllable.compose()

    @override
    def clear(self) -> None:
        self._syllable.clear()

    @override
    def pop(self) -> Optional[str]:
        return self._syllable.pop()

    @override
    def flush(self) -> Sequence[str]:
        return self._syllable.compose_and_clear()

    @override
    def add(self, text: str) -> Sequence[str]:
        if 1 != len(text):
            raise ValueError("Only one character must be added")

        hangul = self._dubeolsik_hangul_map.get(text, text)
        assert 1 == len(hangul)

        return self._syllable.push(hangul)

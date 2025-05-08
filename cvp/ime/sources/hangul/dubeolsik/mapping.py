# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Dict


@lru_cache
def create_dubeolsik_hangul_consonants_mapping() -> MappingProxyType[str, str]:
    return MappingProxyType(
        {
            "q": "ㅂ",
            "w": "ㅈ",
            "e": "ㄷ",
            "r": "ㄱ",
            "t": "ㅅ",
            "a": "ㅁ",
            "s": "ㄴ",
            "d": "ㅇ",
            "f": "ㄹ",
            "g": "ㅎ",
            "z": "ㅋ",
            "x": "ㅌ",
            "c": "ㅊ",
            "v": "ㅍ",
            "Q": "ㅃ",
            "W": "ㅉ",
            "E": "ㄸ",
            "R": "ㄲ",
            "T": "ㅆ",
            "A": "ㅁ",
            "S": "ㄴ",
            "D": "ㅇ",
            "F": "ㄹ",
            "G": "ㅎ",
            "Z": "ㅋ",
            "X": "ㅌ",
            "C": "ㅊ",
            "V": "ㅍ",
        }
    )


@lru_cache
def create_dubeolsik_hangul_vowels_mapping() -> MappingProxyType[str, str]:
    return MappingProxyType(
        {
            "y": "ㅛ",
            "u": "ㅕ",
            "i": "ㅑ",
            "o": "ㅐ",
            "p": "ㅔ",
            "h": "ㅗ",
            "j": "ㅓ",
            "k": "ㅏ",
            "l": "ㅣ",
            "b": "ㅠ",
            "n": "ㅜ",
            "m": "ㅡ",
            "Y": "ㅛ",
            "U": "ㅕ",
            "I": "ㅑ",
            "O": "ㅒ",
            "P": "ㅖ",
            "H": "ㅗ",
            "J": "ㅓ",
            "K": "ㅏ",
            "L": "ㅣ",
            "B": "ㅠ",
            "N": "ㅜ",
            "M": "ㅡ",
        }
    )


@lru_cache
def create_dubeolsik_hangul_mapping() -> MappingProxyType[str, str]:
    consonants = create_dubeolsik_hangul_consonants_mapping()
    vowels = create_dubeolsik_hangul_vowels_mapping()
    total: Dict[str, str] = dict()
    total.update(consonants)
    total.update(vowels)
    return MappingProxyType(total)

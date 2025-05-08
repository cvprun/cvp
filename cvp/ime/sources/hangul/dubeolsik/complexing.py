# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType

ComplexingMappingType = MappingProxyType[str, MappingProxyType[str, str]]


@lru_cache
def create_consonants_complexing() -> ComplexingMappingType:
    return MappingProxyType(
        {
            "ㄱ": MappingProxyType(
                {
                    "ㅅ": "ㄳ",
                }
            ),
            "ㄴ": MappingProxyType(
                {
                    "ㅈ": "ㄵ",
                    "ㅎ": "ㄶ",
                }
            ),
            "ㄹ": MappingProxyType(
                {
                    "ㄱ": "ㄺ",
                    "ㅁ": "ㄻ",
                    "ㅂ": "ㄼ",
                    "ㅅ": "ㄽ",
                    "ㅌ": "ㄾ",
                    "ㅍ": "ㄿ",
                    "ㅎ": "ㅀ",
                }
            ),
            "ㅂ": MappingProxyType(
                {
                    "ㅅ": "ㅄ",
                }
            ),
        }
    )


@lru_cache
def create_vowels_complexing() -> ComplexingMappingType:
    return MappingProxyType(
        {
            "ㅗ": MappingProxyType(
                {
                    "ㅏ": "ㅘ",
                    "ㅐ": "ㅙ",
                    "ㅣ": "ㅚ",
                }
            ),
            "ㅜ": MappingProxyType(
                {
                    "ㅓ": "ㅝ",
                    "ㅔ": "ㅞ",
                    "ㅣ": "ㅟ",
                }
            ),
            "ㅡ": MappingProxyType(
                {
                    "ㅣ": "ㅢ",
                }
            ),
        }
    )

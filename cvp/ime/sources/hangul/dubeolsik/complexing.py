# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Tuple

ComplexMappingType = MappingProxyType[str, MappingProxyType[str, str]]
SplitMappingType = MappingProxyType[str, Tuple[str, str]]


@lru_cache
def create_jongseong_complex_mapping() -> ComplexMappingType:
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
def create_jongseong_split_mapping() -> SplitMappingType:
    return MappingProxyType(
        {
            "ㄳ": ("ㄱ", "ㅅ"),
            "ㄵ": ("ㄴ", "ㅈ"),
            "ㄶ": ("ㄴ", "ㅎ"),
            "ㄺ": ("ㄹ", "ㄱ"),
            "ㄻ": ("ㄹ", "ㅁ"),
            "ㄼ": ("ㄹ", "ㅂ"),
            "ㄽ": ("ㄹ", "ㅅ"),
            "ㄾ": ("ㄹ", "ㅌ"),
            "ㄿ": ("ㄹ", "ㅍ"),
            "ㅀ": ("ㄹ", "ㅎ"),
            "ㅄ": ("ㅂ", "ㅅ"),
        }
    )


@lru_cache
def create_vowels_complex_mapping() -> ComplexMappingType:
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


@lru_cache
def create_vowels_split_mapping() -> SplitMappingType:
    return MappingProxyType(
        {
            "ㅘ": ("ㅗ", "ㅏ"),
            "ㅙ": ("ㅗ", "ㅐ"),
            "ㅚ": ("ㅗ", "ㅣ"),
            "ㅝ": ("ㅜ", "ㅓ"),
            "ㅞ": ("ㅜ", "ㅔ"),
            "ㅟ": ("ㅜ", "ㅣ"),
            "ㅢ": ("ㅡ", "ㅣ"),
        }
    )

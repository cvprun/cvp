# -*- coding: utf-8 -*-

from enum import StrEnum, unique
from functools import lru_cache
from re import Pattern
from re import compile as re_compile
from types import MappingProxyType
from typing import Callable, Dict, Final


@unique
class CaseType(StrEnum):
    camel_case = "camelCase"
    pascal_case = "PascalCase"
    mixed_case = "MixedCase"
    snake_case = "snake_case"
    upper_case = "UPPER_CASE"
    kebab_case = "kebab-case"
    title_kebab_case = "Title-Kebab-Case"
    space_case = "space case"
    title_case = "Title Case"
    sentence_case = "Sentence case"
    dot_case = "dot.case"


CaseConvertCallable = Callable[[str], str]
CaseConvertDict = Dict[CaseType, CaseConvertCallable]
CaseConvertMapping = MappingProxyType[CaseType, CaseConvertCallable]

_CAMELCASE_TO_SNAKECASE1: Final[Pattern] = re_compile(r"([A-Z][A-Z]+)([A-Z][a-z0-9]+)")
_CAMELCASE_TO_SNAKECASE2: Final[Pattern] = re_compile(r"([a-z0-9])([A-Z])")

_DELIMITER_PATTERN = re_compile(r"[ .-]")
_NAMESPACE_SEPARATOR_PATTERN = re_compile(r"::")
_CONSECUTIVE_UPPER_PATTERN = re_compile(r"([A-Z]+)([A-Z][a-z])")
_CAMEL_CASE_BOUNDARY_PATTERN = re_compile(r"([a-z\d])([A-Z])")


def camelcase_to_snakecase(name: str) -> str:
    s1 = _CAMELCASE_TO_SNAKECASE1.sub(r"\1_\2", name)
    s2 = _CAMELCASE_TO_SNAKECASE2.sub(r"\1_\2", s1)
    return s2.lower()


def camel_case(text: str) -> str:
    # Replace spaces, dots, and hyphens with underscores
    text = _DELIMITER_PATTERN.sub("_", text)

    # If no underscores and has lowercase, just lowercase first char
    if "_" not in text and any(c.islower() for c in text):
        return text[0].lower() + text[1:] if text else str()

    # Split by underscore and capitalize each word except first
    parts = text.split("_")
    if not parts:
        return str()

    return parts[0].lower() + "".join(part.capitalize() for part in parts[1:])


def pascal_case(text: str) -> str:
    camel = camel_case(text)
    return camel[0].upper() + camel[1:] if camel else str()


def mixed_case(text: str) -> str:
    return pascal_case(text)


def snake_case(text: str) -> str:
    # Replace :: with /
    text = _NAMESPACE_SEPARATOR_PATTERN.sub("/", text)

    # Insert underscore between consecutive uppercase letters followed by lowercase
    text = _CONSECUTIVE_UPPER_PATTERN.sub(r"\1_\2", text)

    # Insert underscore between lowercase/digit and uppercase
    text = _CAMEL_CASE_BOUNDARY_PATTERN.sub(r"\1_\2", text)

    # Replace spaces, dots, and hyphens with underscores
    text = _DELIMITER_PATTERN.sub("_", text)

    return text.lower()


def upper_case(text: str) -> str:
    return snake_case(text).upper()


def kebab_case(text: str) -> str:
    return snake_case(text).replace("_", "-")


def title_kebab_case(text: str) -> str:
    return title_case(text).replace(" ", "-")


def space_case(text: str) -> str:
    return snake_case(text).replace("_", " ")


def title_case(text: str) -> str:
    space_cased = space_case(text)
    return " ".join(part.capitalize() for part in space_cased.split())


def sentence_case(text: str) -> str:
    space_cased = space_case(text)
    return space_cased.capitalize() if space_cased else ""


def dot_case(text: str) -> str:
    return snake_case(text).replace("_", ".")


def _create_case_function_mapping() -> CaseConvertDict:
    return {
        CaseType.camel_case: camel_case,
        CaseType.pascal_case: pascal_case,
        CaseType.mixed_case: mixed_case,
        CaseType.snake_case: snake_case,
        CaseType.upper_case: upper_case,
        CaseType.kebab_case: kebab_case,
        CaseType.title_kebab_case: title_kebab_case,
        CaseType.space_case: space_case,
        CaseType.title_case: title_case,
        CaseType.sentence_case: sentence_case,
        CaseType.dot_case: dot_case,
    }


@lru_cache
def _case_function_mapping() -> CaseConvertMapping:
    return MappingProxyType(_create_case_function_mapping())


CASE_FUNCTION_MAPPING: Final[CaseConvertMapping] = _case_function_mapping()


def convert_case(case_type: CaseType, text: str) -> str:
    return CASE_FUNCTION_MAPPING[case_type](text)

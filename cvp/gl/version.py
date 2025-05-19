# -*- coding: utf-8 -*-

from re import Pattern
from re import compile as re_compile
from typing import Final, NamedTuple

from OpenGL import GL

VERSION_REGEX: Final[Pattern[str]] = re_compile(r"(\d+\.\d+)(.*)")


class GlVersion(NamedTuple):
    major: int
    minor: int
    extra: str


def get_version() -> str:
    result = GL.glGetString(GL.GL_VERSION)
    if result is None:
        return str()

    assert isinstance(result, bytes)
    return str(result, encoding="utf-8")


def parse_version(text: str) -> GlVersion:
    match = VERSION_REGEX.match(text.strip())
    if match is None:
        raise ValueError(f"Invalid version string: {text}")

    prefix = match.group(1)
    suffix = match.group(2)
    major, minor = prefix.split(".", 1)
    return GlVersion(int(major), int(minor), suffix.strip())


def get_version_tuple() -> GlVersion:
    return parse_version(get_version())

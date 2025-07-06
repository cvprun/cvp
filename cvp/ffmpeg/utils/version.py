# -*- coding: utf-8 -*-

from subprocess import check_output
from typing import NamedTuple, Optional


class FFmpegVersion(NamedTuple):
    major: int
    minor: int
    patch: int
    extra: Optional[str] = None
    version_full: Optional[str] = None
    copyright_full: Optional[str] = None

    @classmethod
    def from_text(cls, version_text: str, copyright_text: Optional[str] = None):
        version_extra = version_text.split("-", maxsplit=1)
        versions = version_extra[0].split(".")
        major_text, minor_text, patch_text = versions
        assert isinstance(major_text, str)
        assert isinstance(minor_text, str)
        assert isinstance(patch_text, str)
        extra = version_extra[1] if 2 <= len(version_extra) else None

        if major_text[0].isnumeric():
            major = int(major_text)
        else:
            assert major_text[1].isnumeric()
            major = int(major_text[1:])  # e.g. 'n7'

        minor = int(minor_text)
        patch = int(patch_text)

        return cls(major, minor, patch, extra, version_text, copyright_text)


def parse_version_output(text: str) -> FFmpegVersion:
    items = text.splitlines(keepends=False)[0].split(maxsplit=3)

    if items[0] != "ffmpeg":
        raise ValueError("Invalid ffmpeg version output")
    if items[1] != "version":
        raise ValueError("Invalid ffmpeg version output")

    version_text = items[2]
    copyright_text = items[3]

    if not copyright_text.startswith("Copyright"):
        raise ValueError("Invalid ffmpeg version output")

    return FFmpegVersion.from_text(version_text, copyright_text)


def inspect_version(ffmpeg="ffmpeg") -> FFmpegVersion:
    cmds = ffmpeg, "-hide_banner", "-version"
    output = check_output(cmds).decode("utf-8")
    return parse_version_output(output)

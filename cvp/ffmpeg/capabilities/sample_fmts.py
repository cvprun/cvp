# -*- coding: utf-8 -*-

from dataclasses import dataclass
from subprocess import check_output
from typing import Final, List, Optional, Sequence

from cvp.ffmpeg.capabilities._parser import (
    FormatLineProtocol,
    parse_ffmpeg_format_output,
)
from cvp.itertools.find import find_element

FFMPEG_SAMPLE_FMTS_HEADER_LINES: Final[Sequence[str]] = ("name   depth",)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -sample_fmts` command."""


@dataclass
class SampleFmt(FormatLineProtocol):
    name: str
    depth: int

    def __repr__(self):
        return f"{self.name} {self.depth}"

    @classmethod
    def from_format_line(cls, line: str, major: Optional[int] = None):
        name_depth = line.split(maxsplit=1)
        assert len(name_depth) == 2
        name = name_depth[0].strip()
        depth = int(name_depth[1].strip())
        return cls(name=name, depth=depth)


def parse_sample_fmts_output(text: str) -> List[SampleFmt]:
    return parse_ffmpeg_format_output(text, FFMPEG_SAMPLE_FMTS_HEADER_LINES, SampleFmt)


def inspect_sample_fmts(ffmpeg="ffmpeg") -> List[SampleFmt]:
    cmds = ffmpeg, "-hide_banner", "-sample_fmts"
    output = check_output(cmds).decode("utf-8")
    return parse_sample_fmts_output(output)


def find_sample_fmt(name: str, ffmpeg="ffmpeg") -> SampleFmt:
    return find_element(inspect_sample_fmts(ffmpeg), lambda x: x.name == name)

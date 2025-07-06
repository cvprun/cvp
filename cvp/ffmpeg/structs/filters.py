# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum
from io import StringIO
from subprocess import check_output
from typing import Final, List, Sequence

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element

FFMPEG_FILTERS_HEADER_LINES: Final[Sequence[str]] = (
    "Filters:",
    "  T.. = Timeline support",
    "  .S. = Slice threading",
    "  ..C = Command support",
    "  A = Audio input/output",
    "  V = Video input/output",
    "  N = Dynamic number and/or type of input/output",
    "  | = Source or sink filter",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -filters` command."""


class FilterInput(StrEnum):
    audio = "A"
    dual_audio = "AA"
    video = "V"
    dual_video = "VV"
    triple_video = "VVV"
    quadruple_video = "VVVV"
    dynamic = "N"
    source = "|"


class FilterOutput(StrEnum):
    audio = "A"
    video = "V"
    dual_video = "VV"
    audio_video = "AV"
    dynamic = "N"
    sink = "|"


@dataclass
class Filter(FormatLineProtocol):
    timeline_support: bool
    slice_threading: bool
    command_support: bool
    name: str
    input: FilterInput
    output: FilterOutput
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write("T" if self.timeline_support else ".")
        buffer.write("S" if self.slice_threading else ".")
        buffer.write("C" if self.command_support else ".")
        buffer.write(f" {self.name}")
        buffer.write(f" {self.input}->{self.output}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str):
        timeline_support = line[1] == "T"
        slice_threading = line[2] == "S"
        command_support = line[3] == "X"

        name_io_desc = line[5:].split(maxsplit=2)
        assert len(name_io_desc) == 3
        name = name_io_desc[0].strip()
        input_, output = name_io_desc[1].strip().split("->")
        desc = name_io_desc[2].strip()

        return cls(
            timeline_support=timeline_support,
            slice_threading=slice_threading,
            command_support=command_support,
            name=name,
            input=FilterInput(input_),
            output=FilterOutput(output),
            description=desc,
        )


def parse_filters_output(text: str) -> List[Filter]:
    return parse_ffmpeg_format_output(text, FFMPEG_FILTERS_HEADER_LINES, Filter)


def inspect_filters(ffmpeg="ffmpeg") -> List[Filter]:
    cmds = ffmpeg, "-hide_banner", "-filters"
    output = check_output(cmds).decode("utf-8")
    return parse_filters_output(output)


def find_filter(name: str, ffmpeg="ffmpeg") -> Filter:
    return find_element(inspect_filters(ffmpeg), lambda x: x.name == name)

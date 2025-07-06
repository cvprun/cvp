# -*- coding: utf-8 -*-

from dataclasses import dataclass
from io import StringIO
from subprocess import check_output
from typing import Final, List, Sequence

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element

FFMPEG_MUXERS_HEADER_LINES: Final[Sequence[str]] = (
    "Formats:",
    " D.. = Demuxing supported",
    " .E. = Muxing supported",
    " ..d = Is a device",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -muxers` command."""


@dataclass
class Muxer(FormatLineProtocol):
    demuxing: bool
    muxing: bool
    device: bool
    name: str
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write("D" if self.demuxing else ".")
        buffer.write("E" if self.muxing else ".")
        buffer.write("d" if self.device else ".")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str):
        demuxing = line[1] == "D"
        muxing = line[2] == "E"
        device = line[3] == "d"
        name_desc = line[5:].split(maxsplit=1)
        assert len(name_desc) == 2
        name = name_desc[0].strip()
        desc = name_desc[1].strip()
        return cls(
            demuxing=demuxing,
            muxing=muxing,
            device=device,
            name=name,
            description=desc,
        )


def parse_muxers_output(text: str) -> List[Muxer]:
    return parse_ffmpeg_format_output(text, FFMPEG_MUXERS_HEADER_LINES, Muxer)


def inspect_muxers(ffmpeg="ffmpeg") -> List[Muxer]:
    cmds = ffmpeg, "-hide_banner", "-muxers"
    output = check_output(cmds).decode("utf-8")
    return parse_muxers_output(output)


def find_muxer(name: str, ffmpeg="ffmpeg") -> Muxer:
    return find_element(inspect_muxers(ffmpeg), lambda x: x.name == name)

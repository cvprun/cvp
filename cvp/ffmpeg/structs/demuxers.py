# -*- coding: utf-8 -*-

from dataclasses import dataclass
from io import StringIO
from subprocess import check_output
from typing import Final, List, Sequence

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element

FFMPEG_DEMUXERS_HEADER_LINES: Final[Sequence[str]] = (
    "Formats:",
    " D.. = Demuxing supported",
    " .E. = Muxing supported",
    " ..d = Is a device",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -demuxers` command."""


@dataclass
class Demuxer(FormatLineProtocol):
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


def parse_demuxers_output(text: str) -> List[Demuxer]:
    return parse_ffmpeg_format_output(text, FFMPEG_DEMUXERS_HEADER_LINES, Demuxer)


def inspect_demuxers(ffmpeg="ffmpeg") -> List[Demuxer]:
    cmds = (ffmpeg, "-hide_banner", "-demuxers")
    output = check_output(cmds).decode("utf-8")
    return parse_demuxers_output(output)


def find_demuxer(name: str, ffmpeg="ffmpeg") -> Demuxer:
    return find_element(inspect_demuxers(ffmpeg), lambda x: x.name == name)

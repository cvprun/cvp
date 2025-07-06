# -*- coding: utf-8 -*-

from dataclasses import dataclass
from io import StringIO
from subprocess import check_output
from typing import Final, List, Optional, Sequence

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output

FFMPEG_DEVICES_HEADER_LINES: Final[Sequence[str]] = (
    "Devices:",
    " D. = Demuxing supported",
    " .E = Muxing supported",
    " --",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -devices` command."""


@dataclass
class Device(FormatLineProtocol):
    demuxing: bool
    muxing: bool
    name: str
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write("D" if self.demuxing else ".")
        buffer.write("E" if self.muxing else ".")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str, major: Optional[int] = None):
        demuxing = line[1] == "D"
        muxing = line[2] == "E"
        name_desc = line[4:].split(maxsplit=1)
        name = name_desc[0].strip()
        desc = name_desc[1].strip() if 2 <= len(name_desc) else str()
        return cls(
            demuxing=demuxing,
            muxing=muxing,
            name=name,
            description=desc,
        )


def parse_devices_output(text: str) -> List[Device]:
    return parse_ffmpeg_format_output(text, FFMPEG_DEVICES_HEADER_LINES, Device)


def inspect_devices(ffmpeg="ffmpeg") -> List[Device]:
    cmds = ffmpeg, "-hide_banner", "-devices"
    output = check_output(cmds).decode("utf-8")
    return parse_devices_output(output)


def find_device(name: str, ffmpeg="ffmpeg") -> Device:
    devices = inspect_devices(ffmpeg)
    filtered_devices = list(filter(lambda x: x.name == name, devices))
    if not filtered_devices:
        raise IndexError(f"Not found device: {name}")
    assert len(filtered_devices) == 1
    return filtered_devices[0]

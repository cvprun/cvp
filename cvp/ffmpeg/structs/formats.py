# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from io import StringIO
from subprocess import check_output
from typing import Dict, Final, List, Sequence
from urllib.parse import urlparse

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element

AUTOMATIC_DETECT_FORMAT: Final[str] = "autodect"

WELL_KNOWN_SCHEME_FORMAT: Final[Dict[str, str]] = {
    "rtmp": "flv",
    "rtsp": "rtsp",
}

FFMPEG_FORMATS_HEADER_LINES: Final[Sequence[str]] = (
    "File formats:",
    " D. = Demuxing supported",
    " .E = Muxing supported",
    " --",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -formats` command."""


@dataclass
class Format(FormatLineProtocol):
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
    def from_format_line(cls, line: str):
        demuxing = line[1] == "D"
        muxing = line[2] == "E"
        name_desc = line[4:].split(maxsplit=1)
        assert len(name_desc) in (1, 2)
        name = name_desc[0].strip()
        desc = name_desc[1].strip() if 2 == len(name_desc) else str()
        return cls(
            demuxing=demuxing,
            muxing=muxing,
            name=name,
            description=desc,
        )


def parse_formats_output(text: str) -> List[Format]:
    return parse_ffmpeg_format_output(text, FFMPEG_FORMATS_HEADER_LINES, Format)


def inspect_formats(ffmpeg="ffmpeg") -> List[Format]:
    cmds = (ffmpeg, "-hide_banner", "-formats")
    output = check_output(cmds).decode("utf-8")
    return parse_formats_output(output)


def find_format(name: str, ffmpeg="ffmpeg") -> Format:
    return find_element(inspect_formats(ffmpeg), lambda x: x.name == name)


def detect_format(url: str, ffmpeg="ffmpeg") -> str:
    if os.path.exists(url):
        ext = os.path.splitext(url)[1]
        return ext[1:] if ext[0] == "." else ext
    else:
        formats = inspect_formats(ffmpeg)
        o = urlparse(url)
        if o.scheme:
            if o.scheme in WELL_KNOWN_SCHEME_FORMAT:
                return WELL_KNOWN_SCHEME_FORMAT[o.scheme]
            try:
                file_format = next(filter(lambda f: f.name == o.scheme, formats))
            except StopIteration:
                raise IndexError(f"Unsupported URL scheme: {o.scheme}")
            else:
                return file_format.name
        else:
            raise NotImplementedError("URL scheme is required")

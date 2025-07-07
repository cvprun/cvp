# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum
from io import StringIO
from subprocess import check_output
from typing import Final, List, Optional, Sequence

from cvp.ffmpeg.capabilities._parser import (
    FormatLineProtocol,
    parse_ffmpeg_format_output,
)
from cvp.itertools.find import find_element

FFMPEG_CODECS_HEADER_LINES: Final[Sequence[str]] = (
    "Codecs:",
    " D..... = Decoding supported",
    " .E.... = Encoding supported",
    " ..V... = Video codec",
    " ..A... = Audio codec",
    " ..S... = Subtitle codec",
    " ...I.. = Intra frame-only codec",
    " ....L. = Lossy compression",
    " .....S = Lossless compression",
    " -------",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -codecs` command."""

FFMPEG_V5_CODECS_HEADER_LINES: Final[Sequence[str]] = (
    "Codecs:",
    " D..... = Decoding supported",
    " .E.... = Encoding supported",
    " ..V... = Video codec",
    " ..A... = Audio codec",
    " ..S... = Subtitle codec",
    " ..D... = Data codec",
    " ..T... = Attachment codec",
    " ...I.. = Intra frame-only codec",
    " ....L. = Lossy compression",
    " .....S = Lossless compression",
    " -------",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -codecs` command."""


class CodecType(StrEnum):
    video = "V"
    audio = "A"
    subtitle = "S"
    data = "D"  # Supported from v5 and above.
    attachment = "T"  # Supported from v5 and above.


@dataclass
class Codec(FormatLineProtocol):
    decoding_supported: bool
    encoding_supported: bool
    type: CodecType
    intra_frame_only_codec: bool
    lossy_compression: bool
    lossless_compression: bool
    name: str
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write(self.type)
        buffer.write("D" if self.decoding_supported else ".")
        buffer.write("E" if self.encoding_supported else ".")
        buffer.write(str(self.type))
        buffer.write("I" if self.intra_frame_only_codec else ".")
        buffer.write("L" if self.lossy_compression else ".")
        buffer.write("S" if self.lossless_compression else ".")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str, major: Optional[int] = None):
        decoding_supported = line[1] == "D"
        encoding_supported = line[2] == "E"
        type_ = CodecType(line[3])
        intra_frame_only_codec = line[4] == "I"
        lossy_compression = line[5] == "L"
        lossless_compression = line[6] == "S"

        name_desc = line[8:].split(maxsplit=1)
        assert len(name_desc) == 2
        name = name_desc[0].strip()
        desc = name_desc[1].strip()

        return cls(
            decoding_supported=decoding_supported,
            encoding_supported=encoding_supported,
            type=type_,
            intra_frame_only_codec=intra_frame_only_codec,
            lossy_compression=lossy_compression,
            lossless_compression=lossless_compression,
            name=name,
            description=desc,
        )


def parse_codecs_output(text: str) -> List[Codec]:
    return parse_ffmpeg_format_output(text, FFMPEG_CODECS_HEADER_LINES, Codec)


def parse_v5_codecs_output(text: str) -> List[Codec]:
    return parse_ffmpeg_format_output(
        text,
        FFMPEG_V5_CODECS_HEADER_LINES,
        Codec,
        major=5,
    )


def inspect_codecs(ffmpeg="ffmpeg") -> List[Codec]:
    cmds = ffmpeg, "-hide_banner", "-codecs"
    output = check_output(cmds).decode("utf-8")
    return parse_codecs_output(output)


def find_codec(name: str, ffmpeg="ffmpeg") -> Codec:
    return find_element(inspect_codecs(ffmpeg), lambda x: x.name == name)

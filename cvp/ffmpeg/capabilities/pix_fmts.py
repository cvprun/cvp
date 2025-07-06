# -*- coding: utf-8 -*-

from dataclasses import dataclass
from io import StringIO
from subprocess import check_output
from typing import Final, List, Optional, Sequence

from cvp.ffmpeg.capabilities._parser import (
    FormatLineProtocol,
    parse_ffmpeg_format_output,
)

FFMPEG_PIX_FMTS_HEADER_LINES: Final[Sequence[str]] = (
    "Pixel formats:",
    "I.... = Supported Input  format for conversion",
    ".O... = Supported Output format for conversion",
    "..H.. = Hardware accelerated format",
    "...P. = Paletted format",
    "....B = Bitstream format",
    "FLAGS NAME            NB_COMPONENTS BITS_PER_PIXEL",
    "-----",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -pix_fmts` command."""


@dataclass
class PixFmt(FormatLineProtocol):
    supported_input_format: bool
    supported_output_format: bool
    hardware_accelerated_format: bool
    paletted_format: bool
    bitstream_format: bool
    name: str
    nb_components: int
    bits_per_pixel: int

    def __repr__(self):
        buffer = StringIO()
        buffer.write("I" if self.supported_input_format else ".")
        buffer.write("O" if self.supported_output_format else ".")
        buffer.write("H" if self.hardware_accelerated_format else ".")
        buffer.write("P" if self.paletted_format else ".")
        buffer.write("B" if self.bitstream_format else ".")
        buffer.write(f" comp={self.nb_components}")
        buffer.write(f" bits={self.bits_per_pixel:<3}")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str, major: Optional[int] = None):
        cols = [c.strip() for c in line.split()]
        assert len(cols) == 4
        flags = cols[0]
        return cls(
            supported_input_format=(flags[0] == "I"),
            supported_output_format=(flags[1] == "O"),
            hardware_accelerated_format=(flags[2] == "H"),
            paletted_format=(flags[3] == "P"),
            bitstream_format=(flags[4] == "B"),
            name=cols[1].strip(),
            nb_components=int(cols[2].strip()),
            bits_per_pixel=int(cols[3].strip()),
        )


def parse_fix_fmts_output(text: str) -> List[PixFmt]:
    return parse_ffmpeg_format_output(text, FFMPEG_PIX_FMTS_HEADER_LINES, PixFmt)


def inspect_pix_fmts(ffmpeg="ffmpeg") -> List[PixFmt]:
    cmds = ffmpeg, "-hide_banner", "-pix_fmts"
    output = check_output(cmds).decode("utf-8")
    return parse_fix_fmts_output(output)


def find_pix_fmt(pixel_format: str, ffmpeg="ffmpeg") -> PixFmt:
    pix_fmts = inspect_pix_fmts(ffmpeg)
    filtered_pix_fmts = list(filter(lambda x: x.name == pixel_format, pix_fmts))
    if not filtered_pix_fmts:
        raise IndexError(f"Not found pixel format: {pixel_format}")
    assert len(filtered_pix_fmts) == 1
    return filtered_pix_fmts[0]


def find_bits_per_pixel(pixel_format: str, ffmpeg="ffmpeg") -> int:
    return find_pix_fmt(pixel_format, ffmpeg).bits_per_pixel

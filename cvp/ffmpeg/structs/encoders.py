# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum
from io import StringIO
from subprocess import check_output
from typing import Final, List, Sequence

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element

FFMPEG_ENCODERS_HEADER_LINES: Final[Sequence[str]] = (
    "Encoders:",
    " V..... = Video",
    " A..... = Audio",
    " S..... = Subtitle",
    " .F.... = Frame-level multithreading",
    " ..S... = Slice-level multithreading",
    " ...X.. = Codec is experimental",
    " ....B. = Supports draw_horiz_band",
    " .....D = Supports direct rendering method 1",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -encoders` command."""


class EncoderType(StrEnum):
    video = "V"
    audio = "A"
    subtitle = "S"


@dataclass
class Encoder(FormatLineProtocol):
    type: EncoderType
    frame_level_multithreading: bool
    slice_level_multithreading: bool
    experimental: bool
    draw_horiz_band: bool
    direct_rendering_m1: bool
    name: str
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write(self.type)
        buffer.write("F" if self.frame_level_multithreading else ".")
        buffer.write("S" if self.slice_level_multithreading else ".")
        buffer.write("X" if self.experimental else ".")
        buffer.write("B" if self.draw_horiz_band else ".")
        buffer.write("D" if self.direct_rendering_m1 else ".")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str):
        type_ = EncoderType(line[1])
        frame_level_multithreading = line[2] == "F"
        slice_level_multithreading = line[3] == "S"
        experimental = line[4] == "X"
        draw_horiz_band = line[5] == "B"
        direct_rendering_m1 = line[6] == "D"
        name_desc = line[8:].split(maxsplit=1)
        assert len(name_desc) == 2
        name = name_desc[0].strip()
        desc = name_desc[1].strip()
        return cls(
            type=type_,
            frame_level_multithreading=frame_level_multithreading,
            slice_level_multithreading=slice_level_multithreading,
            experimental=experimental,
            draw_horiz_band=draw_horiz_band,
            direct_rendering_m1=direct_rendering_m1,
            name=name,
            description=desc,
        )


def parse_encoders_output(text: str) -> List[Encoder]:
    return parse_ffmpeg_format_output(text, FFMPEG_ENCODERS_HEADER_LINES, Encoder)


def inspect_encoders(ffmpeg="ffmpeg") -> List[Encoder]:
    cmds = (ffmpeg, "-hide_banner", "-encoders")
    output = check_output(cmds).decode("utf-8")
    return parse_encoders_output(output)


def find_encoder(name: str, ffmpeg="ffmpeg") -> Encoder:
    return find_element(inspect_encoders(ffmpeg), lambda x: x.name == name)

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from subprocess import check_output
from typing import Final, List, Sequence, Tuple

from cvp.ffmpeg.structs._parser import FormatLineProtocol, parse_ffmpeg_format_output
from cvp.itertools.find import find_element, find_index

FFMPEG_INDIVIDUAL_CHANNELS_HEADER_LINES: Final[Sequence[str]] = (
    "Individual channels:",
    "NAME           DESCRIPTION",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -layouts` command."""

FFMPEG_STANDARD_CHANNEL_LAYOUTS_HEADER_LINES: Final[Sequence[str]] = (
    "Standard channel layouts:",
    "NAME           DECOMPOSITION",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -layouts` command."""


@dataclass
class IndividualChannel(FormatLineProtocol):
    name: str
    description: str

    def __repr__(self):
        return f"{self.name} {self.description}"

    @classmethod
    def from_format_line(cls, line: str):
        name_desc = line.split(maxsplit=1)
        assert len(name_desc) == 2
        name = name_desc[0].strip()
        desc = name_desc[1].strip()
        return cls(name=name, description=desc)


@dataclass
class Layout(FormatLineProtocol):
    name: str
    decomposition: List[str]

    def __repr__(self):
        return f"{self.name} {self.decomposition}"

    @classmethod
    def from_format_line(cls, line: str):
        name_desc = line.split(maxsplit=1)
        assert len(name_desc) == 2
        name = name_desc[0].strip()
        decomposition = name_desc[1].strip().split("+")
        return cls(name=name, decomposition=decomposition)


def parse_layouts_output(text: str) -> Tuple[List[IndividualChannel], List[Layout]]:
    lines = text.splitlines()
    empty_line_index = find_index(lines, lambda x: not x)
    layouts_begin_index = empty_line_index + 1

    individual_channels_lines = lines[:empty_line_index]
    standard_channel_layouts_lines = lines[layouts_begin_index:]

    individual_channels = parse_ffmpeg_format_output(
        "\n".join(individual_channels_lines),
        FFMPEG_INDIVIDUAL_CHANNELS_HEADER_LINES,
        IndividualChannel,
    )
    standard_channel_layouts = parse_ffmpeg_format_output(
        "\n".join(standard_channel_layouts_lines),
        FFMPEG_STANDARD_CHANNEL_LAYOUTS_HEADER_LINES,
        Layout,
    )
    return individual_channels, standard_channel_layouts


def inspect_layouts(ffmpeg="ffmpeg") -> Tuple[List[IndividualChannel], List[Layout]]:
    cmds = ffmpeg, "-hide_banner", "-layouts"
    output = check_output(cmds).decode("utf-8")
    return parse_layouts_output(output)


def find_individual_channel(name: str, ffmpeg="ffmpeg") -> IndividualChannel:
    individual_channels, _ = inspect_layouts(ffmpeg)
    return find_element(individual_channels, lambda x: x.name == name)


def find_layout(name: str, ffmpeg="ffmpeg") -> Layout:
    _, standard_channel_layouts = inspect_layouts(ffmpeg)
    return find_element(standard_channel_layouts, lambda x: x.name == name)


def find_layout_decomposition(name: str, ffmpeg="ffmpeg") -> List[IndividualChannel]:
    individual_channels, standard_channel_layouts = inspect_layouts(ffmpeg)
    individual_channels_map = {c.name: c for c in individual_channels}
    layout = find_element(standard_channel_layouts, lambda x: x.name == name)
    return [individual_channels_map[d] for d in layout.decomposition]

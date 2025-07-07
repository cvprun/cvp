# -*- coding: utf-8 -*-

from dataclasses import dataclass
from subprocess import check_output
from typing import List

from cvp.itertools.find import find_element


@dataclass
class Color:
    name: str
    color: str

    def __repr__(self):
        return f"{self.name} {self.color}"


def parse_colors_output(text: str) -> List[Color]:
    result = list()
    for line in text.splitlines(keepends=False):
        name_color = line.split(maxsplit=1)
        assert 2 == len(name_color)
        name = name_color[0]
        color = name_color[1]
        assert color[0] == "#"
        if name == "name" and color == "#RRGGBB":
            continue
        result.append(Color(name, color))
    return result


def inspect_colors(ffmpeg="ffmpeg") -> List[Color]:
    cmds = ffmpeg, "-hide_banner", "-colors"
    output = check_output(cmds).decode("utf-8")
    return parse_colors_output(output)


def find_color(name: str, ffmpeg="ffmpeg") -> Color:
    return find_element(inspect_colors(ffmpeg), lambda x: x.name == name)

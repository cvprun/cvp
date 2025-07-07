# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass, field
from io import StringIO
from subprocess import check_output
from typing import List


@dataclass
class BuildConf:
    configuration: List[str] = field(default_factory=list)

    def __repr__(self):
        buffer = StringIO()
        for conf in self.configuration:
            buffer.write(conf)
            buffer.write("\n")
        return buffer.getvalue()


def parse_build_conf_output(text: str) -> BuildConf:
    lines = deque(text.splitlines())
    begin = False

    while lines:
        line = lines.popleft()
        if not line:
            continue

        if line.strip().endswith("configuration:"):
            begin = True
            break

    if not begin:
        raise ValueError("Could not find build configuration")

    result = BuildConf()
    while lines:
        if line := lines.popleft():
            result.configuration.append(line.strip())
        else:
            break
    return result


def inspect_build_conf(ffmpeg="ffmpeg") -> BuildConf:
    cmds = ffmpeg, "-hide_banner", "-buildconf"
    output = check_output(cmds).decode("utf-8")
    return parse_build_conf_output(output)


def startswith_build_conf(prefix: str, ffmpeg="ffmpeg") -> str:
    build_conf = inspect_build_conf(ffmpeg)
    for conf in build_conf.configuration:
        if conf.startswith(prefix):
            return conf
    raise IndexError("Not found conf")

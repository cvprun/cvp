# -*- coding: utf-8 -*-

from subprocess import check_output
from typing import List

from cvp.ffmpeg.capabilities.version import inspect_version


def parse_dispositions_output(text: str) -> List[str]:
    return [line.strip() for line in text.splitlines()]


def inspect_dispositions(ffmpeg="ffmpeg") -> List[str]:
    cmds = ffmpeg, "-hide_banner", "-dispositions"
    output = check_output(cmds).decode("utf-8")
    if 5 <= inspect_version(ffmpeg).major:
        return parse_dispositions_output(output)
    else:
        raise NotImplementedError("Not supported in FFmpeg versions older than 5.0")

# -*- coding: utf-8 -*-

from collections import deque
from subprocess import check_output
from typing import List


def parse_hwaccels_output(text: str) -> List[str]:
    lines = deque(text.splitlines())
    begin = False

    while lines:
        line = lines.popleft()
        if not line:
            continue

        if line.strip().endswith("Hardware acceleration methods:"):
            begin = True
            break

    if not begin:
        raise ValueError("Could not find hardware acceleration methods")

    result = list()
    while lines:
        if line := lines.popleft().strip():
            result.append(line)
        else:
            break
    return result


def inspect_hwaccels(ffmpeg="ffmpeg") -> List[str]:
    cmds = ffmpeg, "-hide_banner", "-hwaccels"
    output = check_output(cmds).decode("utf-8")
    return parse_hwaccels_output(output)

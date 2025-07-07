# -*- coding: utf-8 -*-

from collections import deque
from subprocess import check_output
from typing import List


def parse_bsfs_output(text: str) -> List[str]:
    lines = deque(text.splitlines())
    begin = False

    while lines:
        line = lines.popleft()
        if not line:
            continue

        if line.strip().endswith("Bitstream filters:"):
            begin = True
            break

    if not begin:
        raise ValueError("Could not find bitstream filters")

    result = list()
    while lines:
        if line := lines.popleft().strip():
            result.append(line)
        else:
            break
    return result


def inspect_bsfs(ffmpeg="ffmpeg") -> List[str]:
    cmds = ffmpeg, "-hide_banner", "-bsfs"
    output = check_output(cmds).decode("utf-8")
    return parse_bsfs_output(output)

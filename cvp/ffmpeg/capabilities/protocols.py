# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass, field
from subprocess import check_output
from typing import List


@dataclass
class Protocols:
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


def parse_protocols_output(text: str) -> Protocols:
    lines = deque(text.splitlines())
    begin = False
    use_input = False
    use_output = False

    while lines:
        line = lines.popleft()
        if not line:
            continue

        if line.strip().endswith("Supported file protocols:"):
            begin = True
            break

    if not begin:
        raise ValueError("Could not find protocols")

    result = Protocols()
    while lines:
        if line := lines.popleft().strip():
            if line == "Input:":
                use_input = True
                use_output = False
            elif line == "Output:":
                use_input = False
                use_output = True
            else:
                if use_input:
                    result.inputs.append(line)
                if use_output:
                    result.outputs.append(line)
        else:
            break

    return result


def inspect_protocols(ffmpeg="ffmpeg") -> Protocols:
    cmds = ffmpeg, "-hide_banner", "-protocols"
    output = check_output(cmds).decode("utf-8")
    return parse_protocols_output(output)


def has_input_protocol(name: str, ffmpeg="ffmpeg") -> bool:
    return name in inspect_protocols(ffmpeg).inputs


def has_output_protocol(name: str, ffmpeg="ffmpeg") -> bool:
    return name in inspect_protocols(ffmpeg).outputs

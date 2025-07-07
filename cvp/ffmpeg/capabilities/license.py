# -*- coding: utf-8 -*-

from subprocess import check_output


def inspect_license(ffmpeg="ffmpeg") -> str:
    cmds = ffmpeg, "-hide_banner", "-L"
    return check_output(cmds).decode("utf-8")

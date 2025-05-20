# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class MpvLogLevel(StrEnum):
    no = auto()
    """disable absolutely all messages."""

    fatal = auto()
    """critical/aborting errors."""

    error = auto()
    """simple errors."""

    warn = auto()
    """possible problems."""

    info = auto()
    """informational message."""

    v = auto()
    """noisy informational message."""

    debug = auto()
    """very noisy technical information."""

    trace = auto()
    """extremely noisy."""

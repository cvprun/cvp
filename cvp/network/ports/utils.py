# -*- coding: utf-8 -*-

from enum import Enum, auto, unique
from typing import Final

# Port range boundaries
MIN_PORT: Final[int] = 0
MAX_PORT: Final[int] = 65535

# Well-known ports range (0-1023)
WELL_KNOWN_MIN: Final[int] = 0
WELL_KNOWN_MAX: Final[int] = 1023

# Registered ports range (1024-49151)
REGISTERED_MIN: Final[int] = 1024
REGISTERED_MAX: Final[int] = 49151

# Ephemeral/Dynamic ports range (49152-65535)
EPHEMERAL_MIN: Final[int] = 49152
EPHEMERAL_MAX: Final[int] = 65535


@unique
class PortCategory(Enum):
    WELL_KNOWN = auto()
    REGISTERED = auto()
    EPHEMERAL = auto()


def is_valid_port(port: int) -> bool:
    return MIN_PORT <= port <= MAX_PORT


def is_well_known_port(port: int) -> bool:
    return WELL_KNOWN_MIN <= port <= WELL_KNOWN_MAX


def is_registered_port(port: int) -> bool:
    return REGISTERED_MIN <= port <= REGISTERED_MAX


def is_ephemeral_port(port: int) -> bool:
    return EPHEMERAL_MIN <= port <= EPHEMERAL_MAX


def is_privileged_port(port: int) -> bool:
    return WELL_KNOWN_MIN <= port <= WELL_KNOWN_MAX


def is_unprivileged_port(port: int) -> bool:
    return REGISTERED_MIN <= port <= MAX_PORT


def get_port_category(port: int) -> PortCategory | None:
    if is_well_known_port(port):
        return PortCategory.WELL_KNOWN
    elif is_registered_port(port):
        return PortCategory.REGISTERED
    elif is_ephemeral_port(port):
        return PortCategory.EPHEMERAL
    return None


def is_in_range(port: int, min_port: int, max_port: int) -> bool:
    return min_port <= port <= max_port


def validate_port(port: int) -> None:
    if not is_valid_port(port):
        raise ValueError(f"Port must be between {MIN_PORT} and {MAX_PORT}, got {port}")


def validate_port_range(min_port: int, max_port: int) -> None:
    if min_port > max_port:
        raise ValueError(f"min_port ({min_port}) must be <= max_port ({max_port})")
    validate_port(min_port)
    validate_port(max_port)

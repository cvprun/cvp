# -*- coding: utf-8 -*-

import logging
from json import dumps, loads
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from sys import stdout
from types import MappingProxyType
from typing import Final, Optional, Sequence, Union

from cvp.logging.variables import (
    DEFAULT_DATEFMT,
    DEFAULT_FORMAT,
    DEFAULT_SIMPLE_LOGGING_FORMAT,
    DEFAULT_SIMPLE_LOGGING_STYLE,
    DEFAULT_STYLE,
    DEFAULT_TIMED_ROTATING_WHEN,
    EXPECTED_LOGS_DIRNAME,
    TimedRotatingWhenLiteral,
    default_logging_config,
)
from cvp.system.environ_keys import CVP_HOME

OFF: Final[int] = logging.CRITICAL + 100

SEVERITY_NAME_CRITICAL: Final[str] = "critical"
SEVERITY_NAME_FATAL: Final[str] = "fatal"
SEVERITY_NAME_ERROR: Final[str] = "error"
SEVERITY_NAME_WARNING: Final[str] = "warning"
SEVERITY_NAME_WARN: Final[str] = "warn"
SEVERITY_NAME_INFO: Final[str] = "info"
SEVERITY_NAME_DEBUG: Final[str] = "debug"
SEVERITY_NAME_NOTSET: Final[str] = "notset"
SEVERITY_NAME_OFF: Final[str] = "off"

SEVERITIES: Final[Sequence[str]] = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_FATAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_WARN,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

UNIQUE_LEVEL_NAMES: Final[Sequence[str]] = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

LEVEL_TO_NAME_MAPPING: Final[MappingProxyType[int, str]] = MappingProxyType(
    {
        logging.CRITICAL: SEVERITY_NAME_CRITICAL,
        logging.ERROR: SEVERITY_NAME_ERROR,
        logging.WARNING: SEVERITY_NAME_WARNING,
        logging.INFO: SEVERITY_NAME_INFO,
        logging.DEBUG: SEVERITY_NAME_DEBUG,
        logging.NOTSET: SEVERITY_NAME_NOTSET,
        OFF: SEVERITY_NAME_OFF,
    }
)

NOTSET_LEVEL_NAME_INDEX: Final[int] = UNIQUE_LEVEL_NAMES.index(SEVERITY_NAME_NOTSET)


def convert_level_number(level: Optional[Union[str, int]] = None) -> int:
    if level is None:
        return logging.DEBUG

    if isinstance(level, str):
        ll = level.lower()
        if ll == SEVERITY_NAME_CRITICAL:
            return logging.CRITICAL
        elif ll == SEVERITY_NAME_FATAL:
            return logging.FATAL
        elif ll == SEVERITY_NAME_ERROR:
            return logging.ERROR
        elif ll == SEVERITY_NAME_WARNING:
            return logging.WARNING
        elif ll == SEVERITY_NAME_WARN:
            return logging.WARN
        elif ll == SEVERITY_NAME_INFO:
            return logging.INFO
        elif ll == SEVERITY_NAME_DEBUG:
            return logging.DEBUG
        elif ll == SEVERITY_NAME_NOTSET:
            return logging.NOTSET
        elif ll == SEVERITY_NAME_OFF:
            return OFF
        else:
            try:
                return int(ll)
            except ValueError:
                raise ValueError(f"Unknown level: {level}")
    elif isinstance(level, int):
        return level
    else:
        raise TypeError(f"Unsupported level type: {type(level)}")


def convert_printable_level(level: Union[str, int]) -> str:
    if isinstance(level, str):
        return level
    if isinstance(level, int):
        if level >= OFF:
            return "Off"
        if level > logging.CRITICAL:
            return "OverCritical"
        if level == logging.CRITICAL:
            return "Critical"
        if level > logging.ERROR:
            return "OverError"
        if level == logging.ERROR:
            return "Error"
        if level > logging.WARNING:
            return "OverWarning"
        if level == logging.WARNING:
            return "Warning"
        if level > logging.INFO:
            return "OverInfo"
        if level == logging.INFO:
            return "Info"
        if level > logging.DEBUG:
            return "OverDebug"
        if level == logging.DEBUG:
            return "Debug"
        if level > logging.NOTSET:
            return "OverNotSet"
        if level == logging.NOTSET:
            return "NotSet"
    return str(level)


def set_root_level(level: Union[str, int]) -> None:
    logging.getLogger().setLevel(convert_level_number(level))


def set_asyncio_level(level: Union[str, int]) -> None:
    logging.getLogger("asyncio").setLevel(convert_level_number(level))


def set_default_logging_config(logs_dirname=EXPECTED_LOGS_DIRNAME) -> None:
    dictConfig(default_logging_config(logs_dirname))


def dumps_default_logging_config(
    cvp_home: Union[str, PathLike[str]],
    logs_dirname=EXPECTED_LOGS_DIRNAME,
) -> str:
    json = dumps(default_logging_config(logs_dirname), indent=4)
    return json.replace(f"${{{CVP_HOME}}}", str(cvp_home))


def loads_logging_config(path: str) -> None:
    with open(path, "rt") as f:
        dictConfig(loads(f.read()))


def add_default_rotate_file_logging(
    prefix: str,
    when: Union[str, TimedRotatingWhenLiteral] = DEFAULT_TIMED_ROTATING_WHEN,
    name: Optional[str] = None,
    level=logging.DEBUG,
) -> None:
    formatter = logging.Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = TimedRotatingFileHandler(prefix, when)
    handler.suffix = "%Y%m%d_%H%M%S.log"
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logging.getLogger(name).addHandler(handler)


def add_default_colored_logging(
    name: Optional[str] = None,
    level=logging.DEBUG,
) -> None:
    from cvp.logging.formatters.colored import ColoredFormatter

    formatter = ColoredFormatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logging.getLogger(name).addHandler(handler)


def add_default_logging(name: Optional[str] = None, level=logging.DEBUG) -> None:
    formatter = logging.Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logging.getLogger(name).addHandler(handler)


def add_simple_logging(name: Optional[str] = None, level=logging.DEBUG) -> None:
    formatter = logging.Formatter(
        fmt=DEFAULT_SIMPLE_LOGGING_FORMAT,
        style=DEFAULT_SIMPLE_LOGGING_STYLE,
    )

    handler = logging.StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logging.getLogger(name).addHandler(handler)

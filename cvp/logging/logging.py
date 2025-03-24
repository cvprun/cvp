# -*- coding: utf-8 -*-

from json import dumps, loads
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
    Formatter,
    StreamHandler,
)
from logging import config as logging_config
from logging import (
    getLogger,
)
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from sys import stdout
from typing import Final, Optional, Sequence, Union

from cvp.logging.variables import (
    CVP_DOWNLOAD_LOGGER_NAME,
    CVP_EVENT_LOGGER_NAME,
    CVP_FLOW_LOGGER_NAME,
    CVP_LOGGER_NAME,
    CVP_MSG_LOGGER_NAME,
    CVP_ONVIF_LOGGER_NAME,
    CVP_PROFILE_LOGGER_NAME,
    CVP_WIDGETS_LOGGER_NAME,
    CVP_WORKER_LOGGER_NAME,
    CVP_WSDL_LOGGER_NAME,
    DEFAULT_DATEFMT,
    DEFAULT_FORMAT,
    DEFAULT_LOGGING_CONFIG,
    DEFAULT_SIMPLE_LOGGING_FORMAT,
    DEFAULT_SIMPLE_LOGGING_STYLE,
    DEFAULT_STYLE,
    DEFAULT_TIMED_ROTATING_WHEN,
    TimedRotatingWhenLiteral,
)
from cvp.system.environ_keys import CVP_HOME

logger = getLogger(CVP_LOGGER_NAME)

download_logger = getLogger(CVP_DOWNLOAD_LOGGER_NAME)
event_logger = getLogger(CVP_EVENT_LOGGER_NAME)
flow_logger = getLogger(CVP_FLOW_LOGGER_NAME)
msg_logger = getLogger(CVP_MSG_LOGGER_NAME)
onvif_logger = getLogger(CVP_ONVIF_LOGGER_NAME)
profile_logger = getLogger(CVP_PROFILE_LOGGER_NAME)
widgets_logger = getLogger(CVP_WIDGETS_LOGGER_NAME)
worker_logger = getLogger(CVP_WORKER_LOGGER_NAME)
wsdl_logger = getLogger(CVP_WSDL_LOGGER_NAME)

OFF: Final[int] = CRITICAL + 100

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

LEVEL_NAMES: Final[Sequence[str]] = [
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
]


def convert_level_number(level: Optional[Union[str, int]] = None) -> int:
    if level is None:
        return DEBUG

    if isinstance(level, str):
        ll = level.lower()
        if ll == SEVERITY_NAME_CRITICAL:
            return CRITICAL
        elif ll == SEVERITY_NAME_FATAL:
            return FATAL
        elif ll == SEVERITY_NAME_ERROR:
            return ERROR
        elif ll == SEVERITY_NAME_WARNING:
            return WARNING
        elif ll == SEVERITY_NAME_WARN:
            return WARN
        elif ll == SEVERITY_NAME_INFO:
            return INFO
        elif ll == SEVERITY_NAME_DEBUG:
            return DEBUG
        elif ll == SEVERITY_NAME_NOTSET:
            return NOTSET
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
        if level > CRITICAL:
            return "OverCritical"
        if level == CRITICAL:
            return "Critical"
        if level > ERROR:
            return "OverError"
        if level == ERROR:
            return "Error"
        if level > WARNING:
            return "OverWarning"
        if level == WARNING:
            return "Warning"
        if level > INFO:
            return "OverInfo"
        if level == INFO:
            return "Info"
        if level > DEBUG:
            return "OverDebug"
        if level == DEBUG:
            return "Debug"
        if level > NOTSET:
            return "OverNotSet"
        if level == NOTSET:
            return "NotSet"
    return str(level)


def set_root_level(level: Union[str, int]) -> None:
    getLogger().setLevel(convert_level_number(level))


def set_asyncio_level(level: Union[str, int]) -> None:
    getLogger("asyncio").setLevel(convert_level_number(level))


def set_default_logging_config() -> None:
    logging_config.dictConfig(DEFAULT_LOGGING_CONFIG)


def dumps_default_logging_config(cvp_home: Union[str, PathLike[str]]) -> str:
    json = dumps(DEFAULT_LOGGING_CONFIG, indent=4)
    return json.replace(f"${{{CVP_HOME}}}", str(cvp_home))


def loads_logging_config(path: str) -> None:
    with open(path, "rt") as f:
        logging_config.dictConfig(loads(f.read()))


def add_default_rotate_file_logging(
    prefix: str,
    when: Union[str, TimedRotatingWhenLiteral] = DEFAULT_TIMED_ROTATING_WHEN,
    name: Optional[str] = None,
    level=DEBUG,
) -> None:
    formatter = Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = TimedRotatingFileHandler(prefix, when)
    handler.suffix = "%Y%m%d_%H%M%S.log"
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger(name).addHandler(handler)


def add_default_colored_logging(name: Optional[str] = None, level=DEBUG) -> None:
    from cvp.logging.formatters.colored import ColoredFormatter

    formatter = ColoredFormatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger(name).addHandler(handler)


def add_default_logging(name: Optional[str] = None, level=DEBUG) -> None:
    formatter = Formatter(
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATEFMT,
        style=DEFAULT_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger(name).addHandler(handler)


def add_simple_logging(name: Optional[str] = None, level=DEBUG) -> None:
    formatter = Formatter(
        fmt=DEFAULT_SIMPLE_LOGGING_FORMAT,
        style=DEFAULT_SIMPLE_LOGGING_STYLE,
    )

    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    getLogger(name).addHandler(handler)

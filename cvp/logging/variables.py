# -*- coding: utf-8 -*-

from typing import Any, Dict, Final, Literal, Sequence, get_args

from cvp.system.environ_keys import CVP_HOME

CVP_LOGGER_NAME: Final[str] = "cvp"  # Project root logger

CVP_DOWNLOAD_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.download"
CVP_EVENT_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.event"
CVP_FLOW_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.flow"
CVP_MSG_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.msg"
CVP_ONVIF_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.onvif"
CVP_PROFILE_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.profile"
CVP_WIDGETS_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.widgets"
CVP_WORKER_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.worker"
CVP_WSDL_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.wsdl"

TimedRotatingWhenLiteral = Literal[
    "S", "M", "H", "D", "W0", "W1", "W2", "W3", "W4", "W5", "W6", "midnight"
]  # W0=Monday
LoggingStyleLiteral = Literal["%", "{", "$"]

TIMED_ROTATING_WHEN: Final[Sequence[str]] = get_args(TimedRotatingWhenLiteral)
DEFAULT_TIMED_ROTATING_WHEN: Final[str] = "D"

DEFAULT_SIMPLE_LOGGING_FORMAT: Final[str] = "{levelname[0]} [{name}] {message}"
DEFAULT_SIMPLE_LOGGING_STYLE: Final[LoggingStyleLiteral] = "{"

FMT_TIME: Final[str] = "%(asctime)s.%(msecs)03d"
FMT_THREAD: Final[str] = "%(process)d/%(thread)s"

DEFAULT_FORMAT = f"{FMT_TIME} {FMT_THREAD} %(name)s %(levelname)s %(message)s"
DEFAULT_DATEFMT: Final[str] = "%Y-%m-%d %H:%M:%S"
DEFAULT_STYLE: Final[LoggingStyleLiteral] = "%"

SIMPLE_FORMAT: Final[str] = "{levelname[0]} {asctime} {name} {message}"
SIMPLE_DATEFMT: Final[str] = "%Y%m%d %H%M%S"
SIMPLE_STYLE: Final[LoggingStyleLiteral] = "{"


def _timed_rotating_file_handler_config(basename: str, backup_count=30):
    return {
        "class": "cvp.logging.handlers.file.TimedRotatingFileHandler",
        "level": "DEBUG",
        "formatter": "default",
        "filename": f"${{{CVP_HOME}}}/logs/{basename}",
        "when": "midnight",
        "interval": 1,
        "backupCount": backup_count,
        "encoding": "utf-8",
        "delay": False,
        "utc": False,
        "suffix": "%Y%m%d_%H%M%S.log",
    }


_simple_formatter = {
    "format": SIMPLE_FORMAT,
    "datefmt": SIMPLE_DATEFMT,
    "style": SIMPLE_STYLE,
}

_stdout_default = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "default",
    "stream": "ext://sys.stdout",
}

_stdout_simple = {
    "class": "logging.StreamHandler",
    "level": "DEBUG",
    "formatter": "simple",
    "stream": "ext://sys.stdout",
}

_file_default = {
    "class": "logging.FileHandler",
    "level": "DEBUG",
    "formatter": "default",
    "filename": "cvp.log",
    "mode": "a",
    "encoding": "utf-8",
    "delay": False,
}

_rotating_file_default = {
    "class": "logging.handlers.RotatingFileHandler",
    "level": "DEBUG",
    "formatter": "default",
    "filename": f"${{{CVP_HOME}}}/logs/cvp_rotating",
    "mode": "a",
    "maxBytes": 10 * 1024 * 1024,
    "backupCount": 10,
    "encoding": "utf-8",
    "delay": False,
}

DEFAULT_LOGGING_CONFIG: Final[Dict[str, Any]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
        "colored": {
            "class": "cvp.logging.formatters.colored.ColoredFormatter",
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
    },
    "handlers": {
        "stdout_colored": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "root_file": _timed_rotating_file_handler_config("__root__"),
        "cvp_file": _timed_rotating_file_handler_config("cvp"),
        "cvp_worker_file": _timed_rotating_file_handler_config("cvp.worker"),
    },
    "loggers": {
        # root logger
        "": {
            "handlers": ["root_file"],
            "level": "DEBUG",
        },
        "OpenGL": {"level": "DEBUG"},
        "asyncio": {"level": "DEBUG"},
        "httpcore": {"level": "DEBUG"},
        "httpx": {"level": "DEBUG"},
        "zeep": {"level": "DEBUG"},
        CVP_LOGGER_NAME: {
            "handlers": ["stdout_colored", "cvp_file"],
            "level": "DEBUG",
            "propagate": 0,
        },
        CVP_DOWNLOAD_LOGGER_NAME: {"level": "DEBUG"},
        CVP_EVENT_LOGGER_NAME: {"level": "INFO"},
        CVP_FLOW_LOGGER_NAME: {"level": "INFO"},
        CVP_MSG_LOGGER_NAME: {"level": "DEBUG"},
        CVP_ONVIF_LOGGER_NAME: {"level": "INFO"},
        CVP_PROFILE_LOGGER_NAME: {"level": "DEBUG"},
        CVP_WIDGETS_LOGGER_NAME: {"level": "INFO"},
        CVP_WORKER_LOGGER_NAME: {
            "handlers": ["stdout_colored", "cvp_worker_file"],
            "level": "DEBUG",
            "propagate": 0,
        },
        CVP_WSDL_LOGGER_NAME: {"level": "INFO"},
    },
}

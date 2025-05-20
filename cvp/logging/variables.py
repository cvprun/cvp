# -*- coding: utf-8 -*-

from typing import Any, Dict, Final, Literal, Sequence, get_args

from cvp.system.environ_keys import CVP_HOME

CVP_LOGGER_NAME: Final[str] = "cvp"  # Project root logger

CVP_CANVAS_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.canvas"
CVP_CHAT_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.chat"
CVP_DOWNLOAD_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.download"
CVP_EVENT_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.event"
CVP_FLOW_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.flow"
CVP_IMGUI_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.imgui"
CVP_MPV_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.mpv"
CVP_MSG_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.msg"
CVP_ONVIF_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.onvif"
CVP_PROFILE_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.profile"
CVP_RENDERER_LOGGER_NAME: Final[str] = f"{CVP_LOGGER_NAME}.renderer"
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

EXPECTED_LOGS_DIRNAME: Final[str] = "logs"


def _timed_rotating_file_handler(
    basename: str,
    logs_dirname=EXPECTED_LOGS_DIRNAME,
    interval=1,
    backup_count=30,
):
    return {
        "class": "cvp.logging.handlers.file.TimedRotatingFileHandler",
        "level": "DEBUG",
        "formatter": "default",
        "filename": f"${{{CVP_HOME}}}/{logs_dirname}/{basename}",
        "when": "midnight",
        "interval": interval,
        "backupCount": backup_count,
        "encoding": "utf-8",
        "delay": False,
        "utc": False,
        "suffix": "%Y%m%d_%H%M%S.log",
    }


def _rotating_file_handler(basename="cvp_rotating", logs_dirname=EXPECTED_LOGS_DIRNAME):
    return {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "DEBUG",
        "formatter": "default",
        "filename": f"${{{CVP_HOME}}}/{logs_dirname}/{basename}",
        "mode": "a",
        "maxBytes": 10 * 1024 * 1024,
        "backupCount": 10,
        "encoding": "utf-8",
        "delay": False,
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


def default_logging_config(logs_dirname=EXPECTED_LOGS_DIRNAME) -> Dict[str, Any]:
    return {
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
            "root_file": _timed_rotating_file_handler("__root__", logs_dirname),
            "cvp_file": _timed_rotating_file_handler("cvp", logs_dirname),
            "cvp_worker_file": _timed_rotating_file_handler("cvp.worker", logs_dirname),
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
            CVP_CHAT_LOGGER_NAME: {"level": "DEBUG"},
            CVP_DOWNLOAD_LOGGER_NAME: {"level": "DEBUG"},
            CVP_EVENT_LOGGER_NAME: {"level": "INFO"},
            CVP_FLOW_LOGGER_NAME: {"level": "INFO"},
            CVP_MSG_LOGGER_NAME: {"level": "DEBUG"},
            CVP_ONVIF_LOGGER_NAME: {"level": "INFO"},
            CVP_PROFILE_LOGGER_NAME: {"level": "DEBUG"},
            CVP_RENDERER_LOGGER_NAME: {"level": "WARNING"},
            CVP_WIDGETS_LOGGER_NAME: {"level": "INFO"},
            CVP_WORKER_LOGGER_NAME: {
                "handlers": ["stdout_colored", "cvp_worker_file"],
                "level": "DEBUG",
                "propagate": 0,
            },
            CVP_WSDL_LOGGER_NAME: {"level": "INFO"},
        },
    }

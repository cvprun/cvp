# -*- coding: utf-8 -*-

from argparse import REMAINDER, ArgumentParser, Namespace, RawDescriptionHelpFormatter
from functools import lru_cache
from os import R_OK, access, getcwd
from os.path import expanduser, isfile, join
from typing import Final, List, Optional, Sequence

from cvp.logging.logging import SEVERITIES, SEVERITY_NAME_INFO
from cvp.system.environ import get_typed_environ_value as get_eval
from cvp.system.environ_keys import (
    CVP_COLORED_LOGGING,
    CVP_DEBUG,
    CVP_DOTENV_PATH,
    CVP_HOME,
    CVP_LOGGING_SEVERITY,
    CVP_LOGGING_STEP,
    CVP_NO_DOTENV,
    CVP_SIMPLE_LOGGING,
    CVP_USE_UVLOOP,
    CVP_VERBOSE,
    PYOPENGL_USE_ACCELERATE,
    SDL_VIDEO_X11_FORCE_EGL,
)
from cvp.variables import (
    CVP_HOME_DIRNAME,
    DOTENV_LOCAL_FILENAME,
    FONT_NAME,
    FONT_SIZE,
    LOGGING_STEP,
)

PROG: Final[str] = "cvp"
DESCRIPTION: Final[str] = "Computer Vision Player"
EPILOG: Final[str] = ""

CMD_PLAYER: Final[str] = "player"
CMD_PLAYER_HELP: Final[str] = "Desktop GUI"
CMD_PLAYER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_PLAYER}
"""

CMD_WORKER: Final[str] = "worker"
CMD_WORKER_HELP: Final[str] = "The flow graph for worker"
CMD_WORKER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_WORKER}
"""

CMD_AGENT: Final[str] = "agent"
CMD_AGENT_HELP: Final[str] = "Background agent"
CMD_AGENT_EPILOG = f"""
Simply usage:
  {PROG} {CMD_AGENT}
"""

CMD_TESTER: Final[str] = "tester"
CMD_TESTER_HELP: Final[str] = "Configuration tester"
CMD_TESTER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_TESTER}
"""

CMDS: Final[Sequence[str]] = CMD_PLAYER, CMD_WORKER, CMD_AGENT, CMD_TESTER
DEFAULT_CMD: Final[str] = CMD_PLAYER

DEFAULT_SEVERITY: Final[str] = SEVERITY_NAME_INFO


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from cvp import __version__

    return __version__


@lru_cache
def cvp_home() -> str:
    return join(expanduser("~"), CVP_HOME_DIRNAME)


def add_dotenv_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--no-dotenv",
        action="store_true",
        default=get_eval(CVP_NO_DOTENV, False),
        help="Do not use dot-env file",
    )
    parser.add_argument(
        "--dotenv-path",
        default=get_eval(CVP_DOTENV_PATH, join(getcwd(), DOTENV_LOCAL_FILENAME)),
        metavar="file",
        help=f"Specifies the dot-env file (default: '{DOTENV_LOCAL_FILENAME}')",
    )


def add_graphic_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--force-egl",
        action="store_true",
        default=get_eval(SDL_VIDEO_X11_FORCE_EGL, False),
        help="A variable controlling whether X11 should use GLX or EGL by default",
    )
    parser.add_argument(
        "--use-accelerate",
        action="store_true",
        default=get_eval(PYOPENGL_USE_ACCELERATE, False),
        help="Enable PyOpenGL hardware acceleration for improved rendering performance",
    )


def add_font_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--font-name",
        type=str,
        default=FONT_NAME,
        metavar="{name}",
        help=f"Default font name (default: '{FONT_NAME}')",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=FONT_SIZE,
        metavar="{pt}",
        help=f"Default font size (default: '{FONT_SIZE}')",
    )


def add_player_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_PLAYER,
        help=CMD_PLAYER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_PLAYER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)


def add_worker_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_WORKER,
        help=CMD_WORKER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_WORKER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)

    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        "--colored-logging",
        "-c",
        action="store_true",
        default=get_eval(CVP_COLORED_LOGGING, False),
        help="Use colored logging",
    )
    logging_group.add_argument(
        "--simple-logging",
        "-s",
        action="store_true",
        default=get_eval(CVP_SIMPLE_LOGGING, False),
        help="Use simple logging",
    )

    parser.add_argument(
        "--logging-step",
        type=int,
        default=get_eval(CVP_LOGGING_STEP, LOGGING_STEP),
        help="An iterative step that emits statistics results to a logger",
    )
    parser.add_argument(
        "--logging-severity",
        choices=SEVERITIES,
        default=get_eval(CVP_LOGGING_SEVERITY, DEFAULT_SEVERITY),
        help=f"Logging severity (default: '{DEFAULT_SEVERITY}')",
    )

    parser.add_argument(
        "--use-uvloop",
        action="store_true",
        default=get_eval(CVP_USE_UVLOOP, False),
        help="Replace the event loop with uvloop",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=get_eval(CVP_DEBUG, False),
        help="Enable debugging mode and change logging severity to 'DEBUG'",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=get_eval(CVP_VERBOSE, 0),
        help="Be more verbose/talkative during the operation",
    )
    parser.add_argument(
        "-D",
        action="store_true",
        default=False,
        help="Same as ['-c', '-d', '-vv'] flags",
    )

    parser.add_argument(
        "opts",
        nargs=REMAINDER,
        help="Worker pipeline arguments",
    )


def add_agent_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_AGENT,
        help=CMD_AGENT_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_AGENT_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)


def add_tester_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_TESTER,
        help=CMD_TESTER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_TESTER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)

    x11_group = parser.add_mutually_exclusive_group()
    x11_group.add_argument(
        "--use-egl",
        action="store_true",
        default=False,
        help="Use EGL for X11",
    )
    x11_group.add_argument(
        "--use-glx",
        action="store_true",
        default=False,
        help="Use GLX for X11",
    )

    accel_group = parser.add_mutually_exclusive_group()
    accel_group.add_argument(
        "--use-accelerate",
        action="store_true",
        default=False,
        help="Enable PyOpenGL hardware acceleration",
    )
    accel_group.add_argument(
        "--no-accelerate",
        action="store_true",
        default=False,
        help="Disable PyOpenGL hardware acceleration",
    )


def default_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )

    add_dotenv_arguments(parser)

    home_path = cvp_home()
    parser.add_argument(
        "--home",
        metavar="dir",
        default=get_eval(CVP_HOME, home_path),
        help=f"{PROG}'s home directory (default: '{home_path}')",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=version(),
    )

    subparsers = parser.add_subparsers(dest="cmd")
    add_player_parser(subparsers)
    add_worker_parser(subparsers)
    add_agent_parser(subparsers)
    add_tester_parser(subparsers)

    return parser


def _load_dotenv(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> None:
    parser = ArgumentParser(add_help=False, allow_abbrev=False, exit_on_error=False)
    add_dotenv_arguments(parser)
    args = parser.parse_known_args(cmdline, namespace)[0]

    assert isinstance(args.no_dotenv, bool)
    assert isinstance(args.dotenv_path, str)

    if args.no_dotenv:
        return
    if not isfile(args.dotenv_path):
        return
    if not access(args.dotenv_path, R_OK):
        return

    try:
        from dotenv import load_dotenv

        load_dotenv(args.dotenv_path)
    except ModuleNotFoundError:
        pass


def _remove_dotenv_attrs(namespace: Namespace) -> Namespace:
    assert isinstance(namespace.no_dotenv, bool)
    assert isinstance(namespace.dotenv_path, str)

    del namespace.no_dotenv
    del namespace.dotenv_path

    assert not hasattr(namespace, "no_dotenv")
    assert not hasattr(namespace, "dotenv_path")

    return namespace


def get_default_arguments(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    # [IMPORTANT] Dotenv related options are processed first.
    _load_dotenv(cmdline, namespace)

    parser = default_argument_parser()
    args = parser.parse_known_args(cmdline, namespace)[0]

    # Remove unnecessary dotenv attrs
    return _remove_dotenv_attrs(args)

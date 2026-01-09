# -*- coding: utf-8 -*-

from argparse import Namespace
from asyncio.exceptions import CancelledError
from functools import lru_cache
from typing import Callable, Dict

from cvp.apps.agent import agent_main
from cvp.apps.cli import cli_main
from cvp.apps.player import player_main
from cvp.apps.tester import tester_main
from cvp.apps.worker import worker_main
from cvp.arguments import CMD_AGENT, CMD_CLI, CMD_PLAYER, CMD_TESTER, CMD_WORKER
from cvp.context.autofixer import AutoFixerError
from cvp.logging.loggers import logger


@lru_cache
def cmd_apps() -> Dict[str, Callable[[Namespace], None]]:
    return {
        CMD_AGENT: agent_main,
        CMD_CLI: cli_main,
        CMD_PLAYER: player_main,
        CMD_TESTER: tester_main,
        CMD_WORKER: worker_main,
    }


def run_app(cmd: str, args: Namespace) -> int:
    apps = cmd_apps()
    app = apps.get(cmd, None)
    if app is None:
        logger.error(f"Unknown app command: {cmd}")
        return 1

    try:
        app(args)
    except AutoFixerError as e:
        logger.warning(f"{e}, Please restart the application")
    except CancelledError:
        logger.debug("An cancelled signal was detected")
    except (KeyboardInterrupt, InterruptedError):
        logger.warning("An interrupt signal was detected")
    except SystemExit as e:
        assert isinstance(e.code, int)
        if e.code != 0:
            logger.warning(f"A system shutdown has been detected ({e.code})")
        return e.code
    except BaseException as e:
        logger.exception(e)
        return 1

    return 0

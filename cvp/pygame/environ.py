# -*- coding: utf-8 -*-

from cvp.system.environ import exchange_env_context
from cvp.system.environ_keys import PYGAME_HIDE_SUPPORT_PROMPT


def hide_pygame_prompt() -> None:
    with exchange_env_context(PYGAME_HIDE_SUPPORT_PROMPT, "1"):
        import pygame  # noqa: F401

# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes._base import BaseMode


@lru_cache
def all_game_mode_types() -> Sequence[Type[BaseMode]]:
    from cvp.apps.player.modes.games.tetrix import TetrixMode

    return (TetrixMode,)

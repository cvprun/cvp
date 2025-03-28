# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes.base import BaseMode
from cvp.apps.player.modes.default import DefaultMode
from cvp.apps.player.modes.preference import PreferenceMode
from cvp.config.sections.appearance import AppMode
from cvp.context.context import Context


@lru_cache
def all_mode_types() -> Sequence[Type[BaseMode]]:
    return (
        PreferenceMode,  # Num.0
        DefaultMode,  # Num.1
    )


def create_modes(context: Context) -> OrderedDict[AppMode, BaseMode]:
    result = OrderedDict[AppMode, BaseMode]()
    for mode_type in all_mode_types():
        result[mode_type.get_mode()] = mode_type(context)
    return result

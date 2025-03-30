# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.chat import ChatMode
from cvp.apps.player.modes.dashboard import DashboardMode
from cvp.apps.player.modes.flow import FlowMode
from cvp.apps.player.modes.preference import PreferenceMode
from cvp.config.sections.appearance import AppMode
from cvp.context.context import Context


@lru_cache
def all_mode_types() -> Sequence[Type[BaseMode]]:
    return (
        PreferenceMode,  # Num.0
        # ----------------------
        DashboardMode,  # Num.1
        ChatMode,
        FlowMode,
    )


def create_modes(context: Context) -> OrderedDict[AppMode, BaseMode]:
    result = OrderedDict[AppMode, BaseMode]()
    for mode_type in all_mode_types():
        result[mode_type.get_mode()] = mode_type(context)
    return result

# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context


@lru_cache
def all_mode_types() -> Sequence[Type[BaseMode]]:
    from cvp.apps.player.modes.chat import ChatMode
    from cvp.apps.player.modes.dashboard import DashboardMode
    from cvp.apps.player.modes.flow import FlowMode
    from cvp.apps.player.modes.games import all_game_mode_types
    from cvp.apps.player.modes.medias import MediasMode
    from cvp.apps.player.modes.onvif import OnvifMode
    from cvp.apps.player.modes.preference import PreferenceMode
    from cvp.apps.player.modes.wsdiscovery import WsDiscoveryMode

    return (
        PreferenceMode,  # Num.0
        # ----------------------
        DashboardMode,  # Num.1
        ChatMode,
        FlowMode,
        MediasMode,
        OnvifMode,
        WsDiscoveryMode,
        # ----------------------
        *all_game_mode_types(),
    )


def create_modes(context: Context):
    result = OrderedDict[str, ModeInterface]()
    for mode_type in all_mode_types():
        result[mode_type.get_mode_name()] = mode_type(context)
    return result

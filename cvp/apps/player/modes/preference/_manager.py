# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes.preference import BasePreference
from cvp.context.context import Context


@lru_cache
def create_preference_widget_types() -> Sequence[Type[BasePreference]]:
    from cvp.apps.player.modes.preference.appearance import AppearancePreference
    from cvp.apps.player.modes.preference.concurrency import ConcurrencyPreference
    from cvp.apps.player.modes.preference.developer import DeveloperPreference
    from cvp.apps.player.modes.preference.directory import DirectoryPreference
    from cvp.apps.player.modes.preference.ffmpeg import FFmpegPreference
    from cvp.apps.player.modes.preference.flow import FlowPreference
    from cvp.apps.player.modes.preference.font import FontPreference
    from cvp.apps.player.modes.preference.keyring import KeyringPreference
    from cvp.apps.player.modes.preference.layout import LayoutPreference
    from cvp.apps.player.modes.preference.logging import LoggingPreference
    from cvp.apps.player.modes.preference.ollama import OllamaPreference
    from cvp.apps.player.modes.preference.overlay import OverlayPreference
    from cvp.apps.player.modes.preference.resource import ResourcePreference
    from cvp.apps.player.modes.preference.supabase import SupabasePreference
    from cvp.apps.player.modes.preference.toast import ToastPreference

    return (
        AppearancePreference,
        ConcurrencyPreference,
        DeveloperPreference,
        DirectoryPreference,
        FFmpegPreference,
        FlowPreference,
        FontPreference,
        KeyringPreference,
        LayoutPreference,
        LoggingPreference,
        OllamaPreference,
        OverlayPreference,
        ResourcePreference,
        SupabasePreference,
        ToastPreference,
    )


def create_preference_widgets(context: Context):
    widget_types = create_preference_widget_types()
    return OrderedDict({wt.get_menu_name(): wt(context) for wt in widget_types})

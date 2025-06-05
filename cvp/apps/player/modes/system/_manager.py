# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.context.context import Context


@lru_cache
def create_system_widget_types() -> Sequence[Type[BaseSystem]]:
    from cvp.apps.player.modes.system.about import AboutSystem

    return (AboutSystem,)


def create_system_widgets(context: Context):
    widget_types = create_system_widget_types()
    return OrderedDict({wt.get_menu_name(): wt(context) for wt in widget_types})

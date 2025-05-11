# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.types.override import override


class ResourcePreference(BasePreference):
    __cvp_menu_name__ = "Resource"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        pass

# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.types.override import override


class ChatPreference(BasePreference):
    __cvp_menu_name__ = "Chat"

    def __init__(self, context: Context):
        super().__init__(context)
        context.config.chat.selected

    @override
    def do_process(self) -> None:
        pass

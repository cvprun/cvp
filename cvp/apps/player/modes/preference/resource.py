# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.types.override import override


class Resource(BasePreference):
    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        pass

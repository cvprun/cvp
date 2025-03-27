# -*- coding: utf-8 -*-

from cvp.apps.player.modes.base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.types.override import override


class DefaultMode(BaseMode):
    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.default

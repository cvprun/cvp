# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.types.override import override


class DashboardMode(BaseMode):
    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.dashboard

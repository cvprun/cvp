# -*- coding: utf-8 -*-

from cvp.apps.player.modes._base import BaseMode


class BaseGameMode(BaseMode):
    __cvp_mode_menus__ = ("Game",)

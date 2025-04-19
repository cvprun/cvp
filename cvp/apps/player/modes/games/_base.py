# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.apps.player.modes._base import BaseMode
from cvp.types.override import override


class BaseGameMode(BaseMode):
    @classmethod
    @override
    def get_mode_menus(cls) -> Sequence[str]:
        return ("Games",)

# -*- coding: utf-8 -*-

from typing import Dict

from cvp.apps.player.modes.base import ModeInterface
from cvp.apps.player.modes.none import NoneMode
from cvp.config.sections.appearance import AppMode
from cvp.renderer.context import RendererContext


def create_modes(context: RendererContext) -> Dict[AppMode, ModeInterface]:
    return {AppMode.none: NoneMode(context)}

# -*- coding: utf-8 -*-

from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.apps.player.modes.text import TextMode
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher(TextMode(TempContext())).run()

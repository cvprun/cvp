# -*- coding: utf-8 -*-

from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.apps.player.modes.preference import PreferenceMode
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher(PreferenceMode(TempContext())).run()

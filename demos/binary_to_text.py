# -*- coding: utf-8 -*-

from cvp.apps.player.modes.binary import BinaryMode
from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher(BinaryMode(TempContext()), force_egl=True, use_accelerate=True).run()

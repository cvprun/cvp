# -*- coding: utf-8 -*-

from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.apps.player.modes.tail import TailMode
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher.from_args(TailMode(TempContext())).run()

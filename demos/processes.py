# -*- coding: utf-8 -*-

from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.apps.player.modes.processes import ProcessesMode
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher.from_args(ProcessesMode(TempContext())).run()

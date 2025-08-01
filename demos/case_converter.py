# -*- coding: utf-8 -*-

from cvp.apps.player.modes.case import CaseMode
from cvp.apps.player.modes.launcher import ModeLauncher
from cvp.context.temp import TempContext

if __name__ == "__main__":
    ModeLauncher.from_args(CaseMode(TempContext())).run()

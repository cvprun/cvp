# -*- coding: utf-8 -*-

from cvp.apps.player.modes.launcher import launch_mode
from cvp.apps.player.modes.games.tetrix import TetrixMode

if __name__ == "__main__":
    launch_mode(TetrixMode)

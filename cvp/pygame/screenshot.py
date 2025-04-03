# -*- coding: utf-8 -*-

from os import PathLike
from typing import Literal

import pygame

from cvp.gl.screenshot import screenshot_as_pillow


def save_screenshot(filename: PathLike[str], channels: Literal[3, 4] = 4) -> None:
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    image = screenshot_as_pillow(width, height, x=0, y=0, channels=channels)
    image.save(filename)

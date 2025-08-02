# -*- coding: utf-8 -*-

from typing import Final

CVP_NO_DOTENV: Final[str] = "CVP_NO_DOTENV"
CVP_DOTENV_PATH: Final[str] = "CVP_NO_DOTENV"

CVP_COLORED_LOGGING: Final[str] = "CVP_COLORED_LOGGING"
CVP_SIMPLE_LOGGING: Final[str] = "CVP_SIMPLE_LOGGING"

CVP_LOGGING_STEP: Final[str] = "CVP_LOGGING_STEP"
CVP_LOGGING_SEVERITY: Final[str] = "CVP_LOGGING_SEVERITY"

CVP_HOME: Final[str] = "CVP_HOME"

CVP_USE_UVLOOP: Final[str] = "CVP_USE_UVLOOP"
CVP_DEBUG: Final[str] = "CVP_DEBUG"
CVP_VERBOSE: Final[str] = "CVP_VERBOSE"

CVP_DISPLAY_HIDDEN: Final[str] = "CVP_DISPLAY_HIDDEN"
CVP_DISPLAY_MINIMIZE: Final[str] = "CVP_DISPLAY_MINIMIZE"

PYOPENGL_USE_ACCELERATE: Final[str] = "PYOPENGL_USE_ACCELERATE"
"""Enable PyOpenGL hardware acceleration for improved rendering performance."""

PYGAME_HIDE_SUPPORT_PROMPT: Final[str] = "PYGAME_HIDE_SUPPORT_PROMPT"
"""
This stops the welcome message popping up in the console that tells you which version
of python, pygame & SDL you are using. Must be set before importing pygame.
"""

SDL_VIDEO_X11_FORCE_EGL: Final[str] = "SDL_VIDEO_X11_FORCE_EGL"
"""A variable controlling whether X11 should use GLX or EGL by default."""

SDL_HINT_VIDEO_ALLOW_SCREENSAVER: Final[str] = "SDL_HINT_VIDEO_ALLOW_SCREENSAVER"
"""Available in SDL 2.0.2 or later."""

SDL_VIDEODRIVER: Final[str] = "SDL_VIDEODRIVER"
"""A variable that decides what video backend to use."""

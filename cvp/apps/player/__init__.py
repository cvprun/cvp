# -*- coding: utf-8 -*-

from argparse import Namespace

from cvp.context.context import Context
from cvp.gl.accelerate import load_accelerate
from cvp.pygame.environ import hide_pygame_prompt


def player_main(args: Namespace) -> None:
    hide_pygame_prompt()

    assert isinstance(args.home, str)

    # You can modify the 'PYOPENGL_USE_ACCELERATE' environment variable
    # when initializing the 'Context' class.
    context = Context(args.home, detect_opengl=True)

    # The value of 'OpenGL.acceleratesupport.ACCELERATE_AVAILABLE' may change
    # due to the 'PYOPENGL_USE_ACCELERATE' environment variable.
    load_accelerate()

    # [IMPORTANT]
    # Do not change the import order!
    # This module calls the 'OpenGL.acceleratesupport' module.
    from cvp.apps.player.app import PlayerApplication

    app = PlayerApplication(context)
    app.start()

# -*- coding: utf-8 -*-

from argparse import Namespace


def tester_main(args: Namespace) -> None:
    from cvp.apps.tester.app import TesterApplication
    from cvp.arguments import get_opengl_config

    opengl_config = get_opengl_config(args)
    force_egl = opengl_config.force_egl
    use_accelerate = opengl_config.use_accelerate

    app = TesterApplication(force_egl, use_accelerate)
    app.start()

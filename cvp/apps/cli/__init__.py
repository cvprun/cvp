# -*- coding: utf-8 -*-

from argparse import Namespace

from cvp.context.context import Context


def cli_main(args: Namespace) -> None:
    assert isinstance(args.home, str)

    context = Context(args.home)

    # [IMPORTANT]
    # Do not change the import order!
    from cvp.apps.agent.cli import CliApplication

    app = CliApplication(context)
    app.start()

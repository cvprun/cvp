# -*- coding: utf-8 -*-

from argparse import Namespace

from cvp.context.context import Context
from cvp.pygame.environ import hide_pygame_prompt


def agent_main(args: Namespace) -> None:
    hide_pygame_prompt()

    assert isinstance(args.home, str)

    context = Context(args.home)

    # [IMPORTANT]
    # Do not change the import order!
    from cvp.apps.agent.app import AgentApplication

    app = AgentApplication(context)
    app.start()

# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.flow.catalog.node.defaults.entrypoint import EntrypointNodeTemplate
from cvp.flow.templates.node import NodeTemplate


def get_default_nodes() -> Sequence[NodeTemplate]:
    return (EntrypointNodeTemplate(),)

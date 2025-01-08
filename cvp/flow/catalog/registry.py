# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.datas.templates.node import NodeTemplate
from cvp.flow.path import FlowPath


def global_registry() -> Dict[FlowPath, NodeTemplate]:
    return dict()

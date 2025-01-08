# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.datas.templates.dtype import Dtype
from cvp.flow.path import FlowPath


def global_registry() -> Dict[FlowPath, Dtype]:
    return dict()

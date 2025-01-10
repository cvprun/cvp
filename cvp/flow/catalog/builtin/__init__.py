# -*- coding: utf-8 -*-

from functools import lru_cache
from types import ModuleType
from typing import Dict, List

from cvp.flow.catalog.builtin import events
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.inspect.member import is_dunder, is_sunder


@lru_cache
def builtin_submodules() -> List[ModuleType]:
    return [events]


@lru_cache
def builtin_templates() -> Dict[str, NodeTemplate]:
    result = dict()
    for module in builtin_submodules():
        assert isinstance(module, ModuleType)

        for key in dir(module):
            # Naming filters
            if is_dunder(key):
                continue
            if is_sunder(key):
                continue

            o = getattr(module, key)

            # Typing filters
            if not isinstance(o, type):
                continue
            if not issubclass(o, NodeTemplate):
                continue

            template = o()
            result[template.path] = template

    return result

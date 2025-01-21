# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, TypeAlias

VariableName: TypeAlias = str
VariableDtypePath: TypeAlias = str
VariableDict = Dict[VariableName, VariableDtypePath]


@dataclass
class FlowStore:
    variables: VariableDict = field(default_factory=dict)

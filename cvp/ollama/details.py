# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ModelDetails:
    modified_at: Optional[datetime] = None
    template: str = field(default_factory=str)
    model_file: str = field(default_factory=str)
    license: str = field(default_factory=str)
    model_info: Dict[str, str] = field(default_factory=dict)
    parameters: str = field(default_factory=str)

    # details
    parent_model: str = field(default_factory=str)
    format: str = field(default_factory=str)
    family: str = field(default_factory=str)
    families: List[str] = field(default_factory=list)
    parameter_size: str = field(default_factory=str)
    quantization_level: str = field(default_factory=str)

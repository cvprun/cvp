# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class ModelDetails:
    modified_at: Optional[datetime] = None
    template: Optional[str] = None
    model_file: Optional[str] = None
    license: Optional[str] = None
    model_info: Optional[dict[str, Any]] = None
    parameters: Optional[str] = None

    # details
    parent_model: Optional[str] = None
    format: Optional[str] = None
    family: Optional[str] = None
    families: Optional[List[str]] = None
    parameter_size: Optional[str] = None
    quantization_level: Optional[str] = None

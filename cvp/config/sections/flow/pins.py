# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.fonts.glyphs.mdi import (
    MDI_ARROW_RIGHT_BOLD,
    MDI_ARROW_RIGHT_BOLD_OUTLINE,
    MDI_CIRCLE,
    MDI_CIRCLE_OUTLINE,
)
from cvp.fonts.size import FontSize

FLOW_PIN_UNCONNECTED_ICON: Final[str] = MDI_ARROW_RIGHT_BOLD_OUTLINE
FLOW_PIN_CONNECTED_ICON: Final[str] = MDI_ARROW_RIGHT_BOLD

DATA_PIN_UNCONNECTED_ICON: Final[str] = MDI_CIRCLE_OUTLINE
DATA_PIN_CONNECTED_ICON: Final[str] = MDI_CIRCLE


@dataclass
class Pins:
    flow_n_icon: str = FLOW_PIN_UNCONNECTED_ICON
    flow_y_icon: str = FLOW_PIN_CONNECTED_ICON

    data_n_icon: str = DATA_PIN_UNCONNECTED_ICON
    data_y_icon: str = DATA_PIN_CONNECTED_ICON

    icon_size: FontSize = FontSize.normal

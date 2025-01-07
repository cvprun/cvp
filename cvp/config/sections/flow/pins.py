# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.fonts.glyphs.mdi import (
    ARROW_RIGHT_BOLD,
    ARROW_RIGHT_BOLD_OUTLINE,
    CIRCLE,
    CIRCLE_OUTLINE,
)
from cvp.fonts.size import FontSize
from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_PIN_CONNECTION_COLOR,
    FLOW_PIN_CONNECTION_THICKNESS,
    FLOW_PIN_HOVERING_COLOR,
    FLOW_PIN_NORMAL_COLOR,
    FLOW_PIN_SELECTED_COLOR,
)

FLOW_PIN_UNCONNECTED_ICON: Final[str] = ARROW_RIGHT_BOLD_OUTLINE
FLOW_PIN_CONNECTED_ICON: Final[str] = ARROW_RIGHT_BOLD
DATA_PIN_UNCONNECTED_ICON: Final[str] = CIRCLE_OUTLINE
DATA_PIN_CONNECTED_ICON: Final[str] = CIRCLE


@dataclass
class Pins:
    flow_n_icon: str = FLOW_PIN_UNCONNECTED_ICON
    flow_y_icon: str = FLOW_PIN_CONNECTED_ICON
    data_n_icon: str = DATA_PIN_UNCONNECTED_ICON
    data_y_icon: str = DATA_PIN_CONNECTED_ICON

    icon_size: FontSize = FontSize.normal

    selected_color: RGBA = FLOW_PIN_SELECTED_COLOR
    hovering_color: RGBA = FLOW_PIN_HOVERING_COLOR
    normal_color: RGBA = FLOW_PIN_NORMAL_COLOR

    connection_color: RGBA = FLOW_PIN_CONNECTION_COLOR
    connection_thickness: float = FLOW_PIN_CONNECTION_THICKNESS

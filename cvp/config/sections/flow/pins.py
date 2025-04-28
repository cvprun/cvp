# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Final

from cvp.assets.fonts import mdi
from cvp.fonts.size import FontSize
from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_PIN_CONNECTION_COLOR,
    FLOW_PIN_CONNECTION_THICKNESS,
    FLOW_PIN_HOVERING_COLOR,
    FLOW_PIN_NORMAL_COLOR,
    FLOW_PIN_SELECTED_COLOR,
)

EXEC_PIN_UNCONNECTED_ICON: Final[str] = mdi.ARROW_RIGHT_BOLD_OUTLINE
EXEC_PIN_CONNECTED_ICON: Final[str] = mdi.ARROW_RIGHT_BOLD
DATA_PIN_UNCONNECTED_ICON: Final[str] = mdi.CIRCLE_BOX_OUTLINE
DATA_PIN_CONNECTED_ICON: Final[str] = mdi.CIRCLE_OFF_OUTLINE
WIRE_UNCONNECTED_ICON: Final[str] = mdi.LINK_OFF
WIRE_CONNECTED_ICON: Final[str] = mdi.LINK
VARIABLE_ICON: Final[str] = mdi.VARIABLE


@dataclass
class Pins:
    exec_n_icon: str = EXEC_PIN_UNCONNECTED_ICON
    exec_y_icon: str = EXEC_PIN_CONNECTED_ICON
    data_n_icon: str = DATA_PIN_UNCONNECTED_ICON
    data_y_icon: str = DATA_PIN_CONNECTED_ICON
    wire_n_icon: str = WIRE_UNCONNECTED_ICON
    wire_y_icon: str = WIRE_CONNECTED_ICON
    variable_icon: str = VARIABLE_ICON

    icon_size: FontSize = FontSize.normal

    selected_color: RGBA = FLOW_PIN_SELECTED_COLOR
    hovering_color: RGBA = FLOW_PIN_HOVERING_COLOR
    normal_color: RGBA = FLOW_PIN_NORMAL_COLOR

    connection_color: RGBA = FLOW_PIN_CONNECTION_COLOR
    connection_thickness: float = FLOW_PIN_CONNECTION_THICKNESS

# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.fonts.size import FontSize
from cvp.types.colors import RGBA
from cvp.types.shapes import Size
from cvp.variables import (
    FLOW_NODE_BACKGROUND_COLOR,
    FLOW_NODE_HOVERING_COLOR,
    FLOW_NODE_HOVERING_THICKNESS,
    FLOW_NODE_ITEM_SPACING,
    FLOW_NODE_LABEL_COLOR,
    FLOW_NODE_LAYOUT_COLOR,
    FLOW_NODE_NORMAL_COLOR,
    FLOW_NODE_NORMAL_THICKNESS,
    FLOW_NODE_ROUNDING,
    FLOW_NODE_SELECTED_COLOR,
    FLOW_NODE_SELECTED_THICKNESS,
    FLOW_NODE_SHOW_LAYOUT,
)


@dataclass
class Nodes:
    show_layout: bool = FLOW_NODE_SHOW_LAYOUT
    item_spacing: Size = FLOW_NODE_ITEM_SPACING

    title_size: FontSize = FontSize.medium
    text_size: FontSize = FontSize.normal
    icon_size: FontSize = FontSize.large

    selected_color: RGBA = FLOW_NODE_SELECTED_COLOR
    hovering_color: RGBA = FLOW_NODE_HOVERING_COLOR
    normal_color: RGBA = FLOW_NODE_NORMAL_COLOR

    selected_thickness: float = FLOW_NODE_SELECTED_THICKNESS
    hovering_thickness: float = FLOW_NODE_HOVERING_THICKNESS
    normal_thickness: float = FLOW_NODE_NORMAL_THICKNESS

    rounding: float = FLOW_NODE_ROUNDING

    background_color: RGBA = FLOW_NODE_BACKGROUND_COLOR
    layout_color: RGBA = FLOW_NODE_LAYOUT_COLOR
    label_color: RGBA = FLOW_NODE_LABEL_COLOR

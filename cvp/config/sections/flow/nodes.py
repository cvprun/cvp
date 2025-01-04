# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.fonts.size import FontSize
from cvp.types.colors import RGBA
from cvp.types.shapes import Size
from cvp.variables import (
    FLOW_NODE_BACKGROUND_COLOR,
    FLOW_NODE_ITEM_SPACING,
    FLOW_NODE_SHOW_LAYOUT,
)


@dataclass
class Nodes:
    show_layout: bool = FLOW_NODE_SHOW_LAYOUT
    item_spacing: Size = FLOW_NODE_ITEM_SPACING

    title_size: FontSize = FontSize.medium
    text_size: FontSize = FontSize.normal
    icon_size: FontSize = FontSize.large

    background_color: RGBA = FLOW_NODE_BACKGROUND_COLOR

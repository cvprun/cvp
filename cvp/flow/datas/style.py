# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.flow.datas.stroke import Stroke
from cvp.palette.basic import BLACK, BLUE, RED
from cvp.palette.tableau import ORANGE
from cvp.types.colors import RGBA


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

    normal_color: RGBA = field(default_factory=lambda: (*BLACK, 0.8))
    hovering_color: RGBA = field(default_factory=lambda: (*ORANGE, 0.9))
    select_color: RGBA = field(default_factory=lambda: (*RED, 0.9))
    layout_color: RGBA = field(default_factory=lambda: (*RED, 0.8))

    pin_connection_color: RGBA = field(default_factory=lambda: (*RED, 0.8))
    pin_connection_thickness: float = 2.0

    selection_box_color: RGBA = field(default_factory=lambda: (*BLUE, 0.3))
    selection_box_thickness: float = 1.0

# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.flow.datas.stroke import Stroke


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

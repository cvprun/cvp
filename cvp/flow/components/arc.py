# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from uuid import uuid4

from cvp.flow.components.anchor import Anchor
from cvp.flow.components.line_type import LineType
from cvp.flow.components.node_pin import NodePin
from cvp.maths.bezier.casteljau.cubic import bezier_cubic_casteljau_points
from cvp.types.shapes import Point, Rect


@dataclass
class Arc:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()

    line_type: LineType = LineType.bezier_cubic
    start_anchor: Anchor = field(default_factory=Anchor)
    end_anchor: Anchor = field(default_factory=Anchor)

    _output: Optional[NodePin] = None
    _input: Optional[NodePin] = None

    _selected: bool = False
    _hovering: bool = False

    _polyline: List[Point] = field(default_factory=list)

    @classmethod
    def from_connect_pair(
        cls,
        output_np: NodePin,
        input_np: NodePin,
        tess_tol: float,
    ):
        result = cls()
        result.output = output_np
        result.input = input_np
        points = result.calc_linear_polyline()
        assert 2 == len(points)
        sx = points[0][0]
        ex = points[1][0]
        delta = abs(ex - sx) / 2.0
        result.start_anchor.point = delta, 0.0
        result.end_anchor.point = -1 * delta, 0.0
        result.update_polyline(tess_tol)
        return result

    @property
    def is_linear_line_type(self) -> bool:
        return self.line_type == LineType.linear

    @property
    def is_bezier_cubic_line_type(self) -> bool:
        return self.line_type == LineType.bezier_cubic

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value: Optional[NodePin]) -> None:
        self._output = value

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value: Optional[NodePin]) -> None:
        self._input = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, value: bool) -> None:
        self._hovering = value

    @property
    def polyline(self):
        return self._polyline

    @polyline.setter
    def polyline(self, value: List[Point]) -> None:
        self._polyline = value

    def get_polyline_roi(self) -> Rect:
        if not self._polyline:
            raise ValueError("The 'polyline' attribute is empty")

        xs = [p[0] for p in self._polyline]
        ys = [p[1] for p in self._polyline]
        return min(xs), min(ys), max(xs), max(ys)

    def get_bezier_cubic_anchors(self) -> Tuple[Point, Point]:
        if len(self.polyline) < 2:
            raise ValueError("At least 2 'polyline' elements are required")

        # The first/last index point is located at the connected pin.
        sx, sy = self.polyline[0]
        ex, ey = self.polyline[-1]

        sax, say = self.start_anchor.point
        eax, eay = self.end_anchor.point

        p1 = sx + sax, sy + say
        p2 = ex + eax, ey + eay

        return p1, p2

    def update_polyline(self, tess_tol: float) -> None:
        points = self.calc_polyline(tess_tol)
        self._polyline.clear()
        self._polyline.extend(points)

    def calc_polyline(self, tess_tol: float) -> List[Point]:
        match self.line_type:
            case LineType.linear:
                return self.calc_linear_polyline()
            case LineType.bezier_cubic:
                return self.calc_bezier_cubic_polyline(tess_tol)
            case _:
                assert False, "Inaccessible section"

    def calc_linear_polyline(self) -> List[Point]:
        if self._input is None:
            raise ValueError("The 'input' attribute is empty")
        if self._output is None:
            raise ValueError("The 'output' attribute is empty")

        snx, sny = self._output.node.node_pos
        six, siy = self._output.pin.icon_pos
        siw, sih = self._output.pin.icon_size
        sx = snx + six + siw / 2
        sy = sny + siy + sih / 2
        sp = sx, sy

        enx, eny = self._input.node.node_pos
        eix, eiy = self._input.pin.icon_pos
        eiw, eih = self._input.pin.icon_size
        ex = enx + eix + eiw / 2
        ey = eny + eiy + eih / 2
        ep = ex, ey

        return [sp, ep]

    def calc_bezier_cubic_polyline(self, tess_tol: float) -> List[Point]:
        points = self.calc_linear_polyline()
        assert 2 == len(points)
        sx, sy = sp = points[0]
        ex, ey = ep = points[1]
        sax, say = self.start_anchor.point
        p2 = sx + sax, sy + say
        eax, eay = self.end_anchor.point
        p3 = ex + eax, ey + eay
        return bezier_cubic_casteljau_points(sp, p2, p3, ep, tess_tol)

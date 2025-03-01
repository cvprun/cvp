# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Optional, Sequence, Tuple
from uuid import uuid4

from type_serialize import Serializable, deserialize, serialize

from cvp.flow.anchor import FlowAnchor
from cvp.flow.line_type import FlowLineType
from cvp.flow.node_pin import FlowNodePin
from cvp.maths.bezier.casteljau.cubic import bezier_cubic_casteljau_points
from cvp.types.override import override
from cvp.types.shapes import Point, Rect


@unique
class FlowArcKeys(StrEnum):
    uuid = auto()
    name_ = "name"
    docs = auto()
    line_type = auto()
    start_anchor = auto()
    end_anchor = auto()


class FlowArc(Serializable):
    Keys = FlowArcKeys

    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        line_type=FlowLineType.bezier_cubic,
        start_anchor: Optional[FlowAnchor] = None,
        end_anchor: Optional[FlowAnchor] = None,
        *,
        output: Optional[FlowNodePin] = None,
        input: Optional[FlowNodePin] = None,
        selected=False,
        hovering=False,
        polyline: Optional[Sequence[Point]] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.docs = docs if docs else str()

        self.line_type = line_type
        self.start_anchor = start_anchor if start_anchor else FlowAnchor()
        self.end_anchor = end_anchor if end_anchor else FlowAnchor()

        self._output = output
        self._input = input

        self._selected = selected
        self._hovering = hovering

        self._polyline = list(polyline if polyline else ())

    @classmethod
    def from_connect_pair(
        cls,
        output_np: FlowNodePin,
        input_np: FlowNodePin,
        tess_tol: float,
        *,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        line_type=FlowLineType.bezier_cubic,
    ):
        result = cls(uuid=uuid, name=name, docs=docs, line_type=line_type)
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

    def __str__(self) -> str:
        """In `cvp.flow` module, this return value is used as a key value."""
        return self.uuid

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.docs == other.docs
            and self.line_type == other.line_type
            and self.start_anchor == other.start_anchor
            and self.end_anchor == other.end_anchor
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.docs = copy(self.docs)
        result.line_type = copy(self.line_type)
        result.start_anchor = copy(self.start_anchor)
        result.end_anchor = copy(self.end_anchor)
        result._output = copy(self._output)
        result._input = copy(self._input)
        result._selected = copy(self._selected)
        result._hovering = copy(self._hovering)
        result._polyline = copy(self._polyline)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.docs = deepcopy(self.docs, memo)
        result.line_type = deepcopy(self.line_type, memo)
        result.start_anchor = deepcopy(self.start_anchor, memo)
        result.end_anchor = deepcopy(self.end_anchor, memo)
        result._output = deepcopy(self._output, memo)
        result._input = deepcopy(self._input, memo)
        result._selected = deepcopy(self._selected, memo)
        result._hovering = deepcopy(self._hovering, memo)
        result._polyline = deepcopy(self._polyline, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self.Keys.uuid: self.uuid,
            self.Keys.name_: self.name,
            self.Keys.docs: self.docs,
            self.Keys.line_type: str(self.line_type),
            self.Keys.start_anchor: serialize(self.start_anchor),
            self.Keys.end_anchor: serialize(self.end_anchor),
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = data.get(self.Keys.uuid, str())
        self.name = data.get(self.Keys.name_, str())
        self.docs = data.get(self.Keys.docs, str())

        if line_type := data.get(self.Keys.line_type):
            self.line_type = FlowLineType(line_type)
        else:
            self.line_type = FlowLineType.bezier_cubic

        if start_anchor := data.get(self.Keys.start_anchor):
            self.start_anchor = deserialize(start_anchor, FlowAnchor)
        else:
            self.start_anchor = FlowAnchor()

        if end_anchor := data.get(self.Keys.end_anchor):
            self.end_anchor = deserialize(end_anchor, FlowAnchor)
        else:
            self.end_anchor = FlowAnchor()

        self._output = None
        self._input = None
        self._selected = False
        self._hovering = False
        self._polyline = list()

    @property
    def is_linear_line_type(self) -> bool:
        return self.line_type == FlowLineType.linear

    @property
    def is_bezier_cubic_line_type(self) -> bool:
        return self.line_type == FlowLineType.bezier_cubic

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value: Optional[FlowNodePin]) -> None:
        self._output = value

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value: Optional[FlowNodePin]) -> None:
        self._input = value

    @property
    def connected(self):
        return self._input is not None and self._output is not None

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
            case FlowLineType.linear:
                return self.calc_linear_polyline()
            case FlowLineType.bezier_cubic:
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

# -*- coding: utf-8 -*-

from cvp.imgui.mouse_button import MouseButton
from cvp.patterns.delta import Delta
from cvp.types.shapes import Point


class ControllerProps:
    def __init__(self):
        self._pan_x = Delta.from_single_value(0.0)
        self._pan_y = Delta.from_single_value(0.0)
        self._zoom = Delta.from_single_value(1.0)

        self._activating = Delta.from_single_value(False)
        self._hovering = Delta.from_single_value(False)
        self._focusing = Delta.from_single_value(False)

        self._shift_down = Delta.from_single_value(False)
        self._ctrl_down = Delta.from_single_value(False)
        self._alt_down = Delta.from_single_value(False)

        self._left_button = MouseButton()
        self._middle_button = MouseButton()
        self._right_button = MouseButton()

        self._mouse_pos = 0.0, 0.0
        self._canvas_pos = 0.0, 0.0
        self._canvas_size = 0.0, 0.0

    @property
    def mx(self):
        return self._mouse_pos[0]

    @property
    def my(self):
        return self._mouse_pos[1]

    @property
    def cx(self):
        return self._canvas_pos[0]

    @property
    def cy(self):
        return self._canvas_pos[1]

    @property
    def cw(self):
        return self._canvas_size[0]

    @property
    def ch(self):
        return self._canvas_size[1]

    @property
    def p1(self):
        return self.cx, self.cy

    @property
    def p2(self):
        return self.cx + self.cw, self.cy + self.ch

    @property
    def canvas_roi(self):
        return self.cx, self.cy, self.cx + self.cw, self.cy + self.ch

    @property
    def pan_x(self):
        return self._pan_x.value

    @pan_x.setter
    def pan_x(self, value: float) -> None:
        self._pan_x.update(value)

    @property
    def pan_y(self):
        return self._pan_y.value

    @pan_y.setter
    def pan_y(self, value: float) -> None:
        self._pan_y.update(value)

    @property
    def zoom(self):
        return self._zoom.value

    @zoom.setter
    def zoom(self, value: float) -> None:
        self._zoom.update(value)

    @property
    def pan(self) -> Point:
        return self._pan_x.value, self._pan_y.value

    @pan.setter
    def pan(self, value: Point) -> None:
        self._pan_x.update(value[0])
        self._pan_y.update(value[1])

    @property
    def activating(self):
        return self._activating.value

    @property
    def hovering(self):
        return self._hovering.value

    @property
    def focusing(self):
        return self._focusing.value

    @property
    def left_dragging(self):
        return self._left_button.is_drag

    @property
    def middle_dragging(self):
        return self._middle_button.is_drag

    @property
    def right_dragging(self):
        return self._right_button.is_drag

    @property
    def left_down(self):
        return self._left_button.is_down

    @property
    def middle_down(self):
        return self._middle_button.is_down

    @property
    def right_down(self):
        return self._right_button.is_down

    @property
    def shift_down(self):
        return self._shift_down.value

    @property
    def ctrl_down(self):
        return self._ctrl_down.value

    @property
    def alt_down(self):
        return self._alt_down.value

    @property
    def only_shift_down(self):
        return self.shift_down and not self.ctrl_down and not self.alt_down

    @property
    def only_ctrl_down(self):
        return not self.shift_down and self.ctrl_down and not self.alt_down

    @property
    def only_alt_down(self):
        return not self.shift_down and not self.ctrl_down and self.alt_down

    @property
    def not_any_modifier_down(self):
        return not self.shift_down and not self.ctrl_down and not self.alt_down

    @property
    def changed_left_down(self) -> bool:
        return self._left_button.changed_down

    @property
    def changed_middle_down(self) -> bool:
        return self._middle_button.changed_down

    @property
    def changed_right_down(self) -> bool:
        return self._right_button.changed_down

    @property
    def changed_left_up(self) -> bool:
        return self._left_button.changed_up

    @property
    def changed_middle_up(self) -> bool:
        return self._middle_button.changed_up

    @property
    def changed_right_up(self) -> bool:
        return self._right_button.changed_up

    @property
    def start_left_dragging(self) -> bool:
        return self._left_button.start_drag

    @property
    def start_middle_dragging(self) -> bool:
        return self._middle_button.start_drag

    @property
    def start_right_dragging(self) -> bool:
        return self._right_button.start_drag

    @property
    def end_left_dragging(self) -> bool:
        return self._left_button.end_drag

    @property
    def end_middle_dragging(self) -> bool:
        return self._middle_button.end_drag

    @property
    def end_right_dragging(self) -> bool:
        return self._right_button.end_drag

    def as_unformatted_text(self) -> str:
        return (
            f"Pen: {self.pan_x:.02f}, {self.pan_y:.02f}\n"
            f"Zoom: {self.zoom:.02f}\n"
            f"Mouse pos: {self.mx:.02f}, {self.my:.02f}\n"
            f"Canvas pos: {self.cx:.02f}, {self.cy:.02f}\n"
            f"Canvas size: {self.cw:.02f}, {self.ch:.02f}\n"
            f"Activating: {self.activating}\n"
            f"Hovering: {self.hovering}\n"
            f"Focusing: {self.focusing}\n"
            f"Left dragging: {self.left_dragging}\n"
            f"Middle dragging: {self.middle_dragging}\n"
            f"Right dragging: {self.right_dragging}\n"
            f"Left down: {self.left_down}\n"
            f"Middle down: {self.middle_down}\n"
            f"Right down: {self.right_down}\n"
            f"Shift down: {self.shift_down}\n"
            f"Ctrl down: {self.ctrl_down}\n"
            f"Alt down: {self.alt_down}\n"
        )

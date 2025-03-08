# -*- coding: utf-8 -*-

from typing import Any, NamedTuple

from cvp.flow.node_pin import FlowNodePin
from cvp.pins.action import Action
from cvp.pins.stream import Stream
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowConnection(NamedTuple):
    output: FlowNodePin
    input: FlowNodePin

    @classmethod
    def reorder_connectable_pins(cls, left: FlowNodePin, right: FlowNodePin):
        if left.node == right.node:
            raise ValueError("Identical nodes cannot be connected")
        if left.pin.stream == right.pin.stream:
            raise ValueError("Identical streams cannot be connected")
        if left.pin.action != right.pin.action:
            raise ValueError("The action of the pins must match")

        if left.pin.stream == Stream.input:
            assert right.pin.stream == Stream.output
            out_conn = right
            in_conn = left
        else:
            assert left.pin.stream == Stream.output
            assert right.pin.stream == Stream.input
            out_conn = left
            in_conn = right

        out_pin = out_conn.pin
        in_pin = in_conn.pin
        assert out_pin.stream == Stream.output
        assert in_pin.stream == Stream.input
        assert out_pin.action == in_pin.action
        action = in_pin.action

        out_type = out_pin.dtype.type
        in_type = in_pin.dtype.type
        assert isinstance(out_type, type)
        assert isinstance(in_type, type)

        if in_type != Any and out_type != Any and not issubclass(out_type, in_type):
            raise TypeError("The output pin must subclass the input pin")

        if action == Action.exec and out_pin.wires:
            raise ValueError("There cannot be multiple output exec pins")
        if action == Action.data and in_pin.wires:
            raise ValueError("There cannot be multiple input data pins")

        return cls(out_conn, in_conn)

    @classmethod
    def is_connectable_pins(cls, left: FlowNodePin, right: FlowNodePin) -> bool:
        try:
            cls.reorder_connectable_pins(left, right)
        except ValueError:
            return False
        else:
            return True

    def __str__(self):
        return f"{self.output}{FLOW_PATH_SEPARATOR}{self.input}"

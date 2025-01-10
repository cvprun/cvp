# -*- coding: utf-8 -*-

from typing import Final

from cvp.flow.datas.action import Action
from cvp.flow.datas.stream import Stream
from cvp.flow.datas.templates.graph import GraphTemplate
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.flow.datas.templates.pin import PinTemplate
from cvp.types.colors import BLUE_RGBA, GREEN_RGBA, RED_RGBA

ARC_FLOW_UUID: Final[str] = "ARC_FLOW"
ARC_DATA_UUID: Final[str] = "ARC_DATA"

PIN_FLOW_OUTPUT_TEMPLATE: Final[PinTemplate] = PinTemplate(
    name="PIN1_NAME",
    docs="PIN1_DOCS",
    dtype="PIN1_DTYPE",
    action=Action.flow,
    stream=Stream.output,
    required=False,
    arcs=[ARC_FLOW_UUID],
)

PIN_DATA_OUTPUT_TEMPLATE: Final[PinTemplate] = PinTemplate(
    name="PIN3_NAME",
    docs="PIN3_DOCS",
    dtype="PIN3_DTYPE",
    action=Action.data,
    stream=Stream.output,
    required=False,
    arcs=[ARC_DATA_UUID],
)

PIN_FLOW_INPUT_TEMPLATE: Final[PinTemplate] = PinTemplate(
    name="PIN2_NAME",
    docs="PIN2_DOCS",
    dtype="PIN2_DTYPE",
    action=Action.flow,
    stream=Stream.input,
    required=False,
    arcs=[ARC_FLOW_UUID],
)

PIN_DATA_INPUT_TEMPLATE: Final[PinTemplate] = PinTemplate(
    name="PIN4_NAME",
    docs="PIN4_DOCS",
    dtype="PIN4_DTYPE",
    action=Action.data,
    stream=Stream.input,
    required=False,
    arcs=[ARC_DATA_UUID],
)

NODE_OUTPUT_TEMPLATE: Final[NodeTemplate] = NodeTemplate(
    name="NODE1_NAME",
    docs="NODE1_DOCS",
    icon="NODE1_ICON",
    color=RED_RGBA,
    pins=[PIN_FLOW_OUTPUT_TEMPLATE, PIN_DATA_OUTPUT_TEMPLATE],
    tags=["NODE1_TAG1"],
)

NODE_INPUT_TEMPLATE: Final[NodeTemplate] = NodeTemplate(
    name="NODE2_NAME",
    docs="NODE2_DOCS",
    icon="NODE2_ICON",
    color=GREEN_RGBA,
    pins=[PIN_FLOW_INPUT_TEMPLATE, PIN_DATA_INPUT_TEMPLATE],
    tags=["NODE2_TAG1"],
)

GRAPH_TEMPLATE = GraphTemplate(
    name="GRAPH1",
    docs="GRAPH1_DOCS",
    icon="GRAPH1_ICON",
    color=BLUE_RGBA,
    nodes=[NODE_OUTPUT_TEMPLATE, NODE_INPUT_TEMPLATE],
    tags=["GRAPH1_TAG1"],
)

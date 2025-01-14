# -*- coding: utf-8 -*-

from typing import Any, Dict, Tuple, TypedDict

from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import DataOutputPinTemplate, FlowOutputPinTemplate
from cvp.fonts.glyphs.mdi import PLAY
from cvp.types.colors import GREEN_RGBA


class EntrypointOutput(TypedDict):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    envs: Dict[str, str]


class Entrypoint(NodeTemplate):
    def __init__(self):
        super().__init__(
            name="entrypoint",
            path="cvp.entrypoint",
            func=None,
            docs="Indicates the starting point of the graph",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(
                FlowOutputPinTemplate(name="start"),
                DataOutputPinTemplate(name="args"),
                DataOutputPinTemplate(name="kwargs"),
                DataOutputPinTemplate(name="envs"),
            ),
            tags=("entrypoint", "main"),
        )

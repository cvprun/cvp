# -*- coding: utf-8 -*-

from cvp.flow.datas.action import Action
from cvp.flow.datas.stream import Stream
from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import PinTemplate
from cvp.fonts.glyphs.mdi import MOVIE_OPEN_PLAY
from cvp.types.colors import WHITE_RGBA


class ButtonEventNode(NodeTemplate):
    def __init__(self):
        super().__init__(
            name=type(self).__name__,
            path=type(self).__module__,
            docs="Button Event Node",
            icon=MOVIE_OPEN_PLAY,
            color=WHITE_RGBA,
            pins=[
                PinTemplate(name="InFlow", action=Action.flow, stream=Stream.input),
                PinTemplate(name="OutFlow", action=Action.flow, stream=Stream.output),
                PinTemplate(name="InData", action=Action.data, stream=Stream.input),
                PinTemplate(name="OutData", action=Action.data, stream=Stream.output),
            ],
            tags=["event"],
        )

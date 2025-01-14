# -*- coding: utf-8 -*-

from cvp.flow.templates.pin_flows import FlowInputPinTemplate, FlowOutputPinTemplate


class EntrypointPinTemplate(FlowInputPinTemplate):
    def __init__(self):
        super().__init__(
            name="entrypoint",
            docs="Indicates the starting point of the flow",
        )


class PrevPinTemplate(FlowInputPinTemplate):
    def __init__(self):
        super().__init__(
            name="prev",
            docs="Marks the starting point of a generic function",
        )


class NextPinTemplate(FlowOutputPinTemplate):
    def __init__(self):
        super().__init__(
            name="next",
            docs="Marks the endpoint of a generic function",
        )

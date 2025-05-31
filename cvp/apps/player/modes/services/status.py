# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.service.item import ServiceItem


class ServicesStatusTab:
    def __init__(self, context: Context):
        self._context = context

    def __call__(self, service: ServiceItem) -> None:
        input_text_disabled("UUID", service.uuid)
        input_text_disabled("Name", service.name)

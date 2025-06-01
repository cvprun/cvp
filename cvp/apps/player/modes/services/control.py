# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.service.item import ServiceItem


class ServicesControl:
    def __init__(self, context: Context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    def __call__(self, service: ServiceItem) -> None:
        input_text_disabled("UUID", service.uuid)
        input_text_disabled("Name", service.name)

        spawnable = self.services.spawnable(service.key)
        stoppable = self.services.stoppable(service.key)
        removable = self.services.removable(service.key)

        if button(f"{mdi.PLAY} Spawn", disabled=not spawnable):
            assert not self.services.has_process(service.key)
            self.services.spawn(service.key)

        imgui.same_line()
        if button(f"{mdi.PAUSE} Interrupt", disabled=not stoppable):
            assert self.services.has_process(service.key)
            self.services.interrupt(service.key)

        imgui.same_line()
        if button(f"{mdi.DELETE} Remove", disabled=not removable):
            assert self.services.has_process(service.key)
            self.services.removable_pop(service.key)

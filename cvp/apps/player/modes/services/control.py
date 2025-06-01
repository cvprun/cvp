# -*- coding: utf-8 -*-

from signal import Signals

from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.button_enum_wrapped import button_enum_wrapped
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.flags.style_var import ITEM_SPACING
from cvp.service.item import ServiceItem


class ServicesControlTab:
    def __init__(self, context: Context):
        self._context = context
        self._signal = Signals.SIGINT

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    def do_remote_control_process(self, service: ServiceItem) -> None:
        label = f"{service.name} ({service.uuid})" if service.name else service.uuid
        imgui.text(label)

        if service.managed:
            pass

        if service.freeze:
            pass

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

    def do_detail_control_process(self, service: ServiceItem) -> None:
        with begin_child_context(
            label="Signals",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y | BORDERS,
        ):
            imgui.push_style_var_x(ITEM_SPACING, 1.0)
            try:
                show_debugging = self.context.debug and 2 <= self.context.verbose
                clicked_index = button_enum_wrapped(
                    enum_type=Signals,
                    show_debugging=show_debugging,
                )
            finally:
                imgui.pop_style_var()

            if clicked_index is not None:
                signum = int(list(Signals)[clicked_index].value)
                self.services.get_process(service.key).psutil.send_signal(signum)

        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text("Signals")

    def __call__(self, service: ServiceItem) -> None:
        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            self.do_detail_control_process(service)
        finally:
            imgui.end_disabled()

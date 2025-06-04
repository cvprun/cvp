# -*- coding: utf-8 -*-

import psutil
from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.widgets.table_mutable_mapping import table_mutable_mapping
from cvp.service.item import ServiceItem, ServiceKey


class ServicesEnvironTab:
    def __init__(self, context: Context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    def __call__(self, service: ServiceItem) -> None:
        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            self.do_environ_process(service.key)
        finally:
            imgui.end_disabled()

    def do_environ_process(self, key: ServiceKey) -> None:
        imgui.text("Environment variables")
        imgui.separator()

        try:
            if process := self.services.get_process(key):
                environ = process.psutil.environ()
            else:
                environ = dict()
        except psutil.NoSuchProcess:
            environ = dict()

        with begin_child_context(
            label="EnvironChild",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y,
        ):
            table_mutable_mapping(
                label="EnvironTable",
                container=environ,
                removable=False,
                show_key=True,
                show_value=True,
                show_actions=False,
                disabled_value=True,
            )

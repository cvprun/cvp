# -*- coding: utf-8 -*-

from typing import Iterable

from imgui_bundle import imgui

from cvp.apps.player.modes.vms.onvif._base import BaseOnvifTab
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.flags import table_column
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.text_colored import text_colored
from cvp.onvif.config import OnvifConfig
from cvp.onvif.service import Service
from cvp.types.override import override
from cvp.wsdl.client import WsdlClient


class OnvifClientTab(BaseOnvifTab):
    __cvp_onvif_tab_name__ = "Client"

    def __init__(self, context: Context):
        super().__init__(context)
        self._update_client_runner = self.context.create_thread_runner(
            self._on_update_client,
        )

    def _on_update_client(self, onvif: OnvifConfig):
        client = self.context.get_onvif_client(onvif)
        client.update_services()
        client.update_wsdl_addresses()
        return client

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @override
    def do_process(self, onvif: OnvifConfig) -> None:
        has_client = self.onvifs.has_client(onvif.key)
        update_client_running = self._update_client_runner.running
        has_error = bool(self._update_client_runner.error)
        disabled_remove = not has_client or update_client_running

        if button("Update ONVIF Client", disabled=update_client_running):
            assert not update_client_running
            self._update_client_runner(onvif)

        imgui.same_line()
        if button("Remove ONVIF Client", disabled=disabled_remove):
            assert has_client
            assert not update_client_running
            self.context.onvifs.pop_client(onvif.key)

        if has_error:
            text_colored(str(self._update_client_runner.error), self.error_color)

        client = self.context.onvifs.get_client(onvif.key)
        if client is None:
            return

        self.do_onvif_service_process(client.services.values())
        self.do_onvif_wsdl_process(client.wsdls)

    @staticmethod
    def do_onvif_service_process(services: Iterable[Service]) -> None:
        imgui.text("Services:")
        if imgui.begin_table("ServicesTable", 3, ONVIF_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Namespace", table_column.WIDTH_STRETCH)
                imgui.table_setup_column("Version", table_column.WIDTH_FIXED)
                imgui.table_setup_column("Address", table_column.WIDTH_STRETCH)
                imgui.table_headers_row()

                for service in services:
                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.text(service["Namespace"])
                    imgui.table_set_column_index(1)
                    version = service["Version"]
                    major = version["Major"]
                    minor = version["Minor"]
                    imgui.text(f"{major}.{minor}")
                    imgui.table_set_column_index(2)
                    imgui.text(service["XAddr"])
            finally:
                imgui.end_table()

    @staticmethod
    def do_onvif_wsdl_process(wsdls: Iterable[WsdlClient]) -> None:
        imgui.text("ONVIF WSDL services:")
        if imgui.begin_table("WsdlTable", 3, ONVIF_TABLE_FLAGS):
            try:
                imgui.table_setup_column("Binding", table_column.WIDTH_FIXED)
                imgui.table_setup_column("Address", table_column.WIDTH_STRETCH)
                imgui.table_headers_row()

                for wsdl in wsdls:
                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.text(wsdl.binding_name)
                    imgui.table_set_column_index(1)
                    imgui.text(wsdl.address if wsdl.address else str())
            finally:
                imgui.end_table()

# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.imgui.flags import table_column
from cvp.imgui.flags.table import ONVIF_TABLE_FLAGS
from cvp.imgui.text_colored import text_colored
from cvp.onvif.onvif import OnvifConfig
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class OnvifServiceTab(TabItem[OnvifConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Service")
        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._update_runner = self.context.pm.create_thread_runner(
            self.on_update_service,
        )

    def on_update_service(self, item: OnvifConfig):
        onvif = self.context.onvifs.get_synced_client(item)
        onvif.update_services()
        onvif.update_wsdl_addresses()
        return onvif

    @override
    def on_item(self, item: OnvifConfig) -> None:
        has_service = item.uuid in self.context.onvifs
        update_running = self._update_runner.running
        has_error = bool(self._update_runner.error)
        disabled_clear = not has_service or update_running

        if button("Update ONVIF Service", disabled=update_running):
            assert not update_running
            self._update_runner(item)

        imgui.same_line()
        if button("Remove ONVIF Service", disabled=disabled_clear):
            assert has_service
            assert not update_running
            self.context.onvifs.pop(item.uuid)

        if has_error:
            text_colored(str(self._update_runner.error), self._error_color)

        onvif = self.context.onvifs.get(item.uuid)
        if onvif is not None:
            imgui.text("Services:")
            if imgui.begin_table("ServicesTable", 3, ONVIF_TABLE_FLAGS):
                try:
                    imgui.table_setup_column("Namespace", table_column.WIDTH_STRETCH)
                    imgui.table_setup_column("Version", table_column.WIDTH_FIXED)
                    imgui.table_setup_column("Address", table_column.WIDTH_STRETCH)
                    imgui.table_headers_row()

                    for service in onvif.services.values():
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

            imgui.text("ONVIF WSDL services:")
            if imgui.begin_table("WsdlTable", 3, ONVIF_TABLE_FLAGS):
                try:
                    imgui.table_setup_column("Binding", table_column.WIDTH_FIXED)
                    imgui.table_setup_column("Address", table_column.WIDTH_STRETCH)
                    imgui.table_headers_row()

                    for wsdl in onvif.wsdls:
                        imgui.table_next_row()
                        imgui.table_set_column_index(0)
                        imgui.text(wsdl.binding_name)
                        imgui.table_set_column_index(1)
                        imgui.text(wsdl.address if wsdl.address else str())
                finally:
                    imgui.end_table()

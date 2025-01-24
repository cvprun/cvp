# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.imgui.button import button
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem

TABLE_FLAGS: Final[int] = (
    imgui.TABLE_SIZING_FIXED_FIT
    | imgui.TABLE_ROW_BACKGROUND
    | imgui.TABLE_BORDERS
    | imgui.TABLE_RESIZABLE
    | imgui.TABLE_REORDERABLE
    | imgui.TABLE_HIDEABLE
)


class OnvifServiceTab(TabItem[OnvifConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Service")
        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._update_runner = self.context.pm.create_thread_runner(
            self.on_update_service,
        )

    def on_update_service(self, item: OnvifConfig):
        onvif = self.context.om.get_synced_client(item, self.context.config.wsdl)
        onvif.update_services()
        onvif.update_wsdl_addresses()
        return onvif

    @override
    def on_item(self, item: OnvifConfig) -> None:
        has_service = item.uuid in self.context.om
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
            self.context.om.pop(item.uuid)

        if has_error:
            imgui.text_colored(str(self._update_runner.error), *self._error_color)

        onvif = self.context.om.get(item.uuid)
        if onvif is not None:
            imgui.text("Services:")
            services_table = imgui.begin_table("ServicesTable", 3, TABLE_FLAGS)
            if services_table.opened:
                imgui.table_setup_column("Namespace", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_setup_column("Version", imgui.TABLE_COLUMN_WIDTH_FIXED)
                imgui.table_setup_column("Address", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_headers_row()

                with services_table:
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

            imgui.text("ONVIF WSDL services:")
            wsdl_table = imgui.begin_table("WsdlTable", 3, TABLE_FLAGS)
            if wsdl_table.opened:
                imgui.table_setup_column("Binding", imgui.TABLE_COLUMN_WIDTH_FIXED)
                imgui.table_setup_column("Address", imgui.TABLE_COLUMN_WIDTH_STRETCH)
                imgui.table_headers_row()

                with wsdl_table:
                    for wsdl in onvif.wsdls:
                        imgui.table_next_row()
                        imgui.table_set_column_index(0)
                        imgui.text(wsdl.binding_name)
                        imgui.table_set_column_index(1)
                        imgui.text(wsdl.address if wsdl.address else str())

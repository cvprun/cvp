# -*- coding: utf-8 -*-

from typing import Final, List, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import MEMORY
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.table import TableFlags
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.modbus.config import ModbusDeviceConfig, ModbusKey
from cvp.modbus.datastore import ModbusDataStore
from cvp.types.override import override


class ModbusMode(BaseMode):
    __cvp_mode_name__ = "Modbus"
    __cvp_mode_icon__ = MEMORY

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS
    _REGISTER_DISPLAY_COUNT: Final[int] = 16

    def __init__(self, context: Context):
        super().__init__(context)

        self._stop_candidate: Optional[ModbusKey] = None
        self._confirm_stop = ConfirmPopup(
            title="Stop Server",
            label="Are you sure you want to stop this server?",
            ok="Stop",
            cancel="No",
            target=self.on_confirm_stop,
        )
        self._confirm_stop_all = ConfirmPopup(
            title="Stop All",
            label="Are you sure you want to stop all servers?",
            ok="Stop All",
            cancel="No",
            target=self.on_confirm_stop_all,
        )

        self._popups = PopupList(
            self._confirm_stop,
            self._confirm_stop_all,
        )

        self._register_offset: int = 0

    @property
    def modbus(self):
        return self.context.modbus

    @property
    def selected_key(self) -> Optional[ModbusKey]:
        key_str = self.selected_submenu
        if key_str:
            return ModbusKey(key_str)
        return None

    @property
    def selected_config(self) -> Optional[ModbusDeviceConfig]:
        key = self.selected_key
        if key and key in self.modbus:
            return self.modbus[key]
        return None

    @property
    def selected_datastore(self) -> Optional[ModbusDataStore]:
        key = self.selected_key
        if key:
            return self.modbus.get_datastore(key)
        return None

    def on_confirm_stop(self, value: bool) -> None:
        if not value:
            return
        if self._stop_candidate:
            self.modbus.stop_server(self._stop_candidate)
            self._stop_candidate = None

    def on_confirm_stop_all(self, value: bool) -> None:
        if not value:
            return
        for key, config in self.modbus.items():
            if config.is_server and self.modbus.has_server(key):
                self.modbus.stop_server(key)

    def _render_server_controls(self) -> None:
        key = self.selected_key
        config = self.selected_config
        has_selection = config is not None and config.is_server

        is_running = False
        if key and has_selection:
            server = self.modbus.get_server(key)
            is_running = server is not None and server.is_running

        if is_running:
            if button("Stop", disabled=not has_selection):
                self._stop_candidate = key
                self._confirm_stop.show()
        else:
            if button("Start", disabled=not has_selection):
                if key:
                    self.modbus.start_server(key)

        imgui.same_line()

        running_count = sum(
            1
            for k, c in self.modbus.items()
            if c.is_server and self.modbus.has_server(k)
        )

        if button("Stop All", disabled=running_count == 0):
            self._confirm_stop_all.show()

    def _render_status(self) -> None:
        imgui.separator()

        server_count = sum(1 for _, c in self.modbus.items() if c.is_server)
        running_count = sum(
            1
            for k, c in self.modbus.items()
            if c.is_server and self.modbus.has_server(k)
        )

        imgui.text(f"Servers: {running_count}/{server_count} running")
        imgui.separator()

    def _render_device_list(self) -> None:
        if imgui.begin_list_box("##DeviceList", FIT_SIZE):
            try:
                for key, config in self.modbus.items():
                    if not config.is_server:
                        continue

                    server = self.modbus.get_server(key)
                    is_running = server is not None and server.is_running
                    status = "[R]" if is_running else "[S]"
                    label = f"{status} {config.name}"

                    selected = str(key) == self.selected_submenu
                    if imgui.selectable(label, selected)[1]:
                        self.selected_submenu = str(key)
            finally:
                imgui.end_list_box()

    def _render_device_details(self, config: ModbusDeviceConfig) -> None:
        imgui.text(f"Name: {config.name}")
        imgui.text(f"Host: {config.host}")
        imgui.text(f"Port: {config.port}")
        imgui.text(f"Unit ID: {config.unit_id}")

        key = config.key
        server = self.modbus.get_server(key)

        imgui.separator()

        if server and server.is_running:
            self.text_success("Status: Running")
            imgui.text(f"Connected Clients: {server.client_count}")
        else:
            self.text_warning("Status: Stopped")

        imgui.separator()
        self._render_datastore_view()

    def _render_datastore_view(self) -> None:
        datastore = self.selected_datastore
        if not datastore:
            imgui.text("No datastore available")
            return

        imgui.text("Data Store")
        imgui.separator()

        _, self._register_offset = imgui.input_int(
            "Offset",
            self._register_offset,
            step=self._REGISTER_DISPLAY_COUNT,
        )
        self._register_offset = max(0, self._register_offset)

        if imgui.begin_tab_bar("##DatastoreTabs"):
            try:
                if imgui.begin_tab_item("Holding Registers")[0]:
                    self._render_holding_registers(datastore)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Input Registers")[0]:
                    self._render_input_registers(datastore)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Coils")[0]:
                    self._render_coils(datastore)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Discrete Inputs")[0]:
                    self._render_discrete_inputs(datastore)
                    imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()

    def _render_holding_registers(self, datastore: ModbusDataStore) -> None:
        offset = self._register_offset
        count = self._REGISTER_DISPLAY_COUNT
        max_addr = min(offset + count, datastore.holding_registers_size)

        if offset >= datastore.holding_registers_size:
            imgui.text("Offset out of range")
            return

        registers = datastore.get_holding_registers(offset, max_addr - offset)
        self._render_register_table("HoldingRegs", offset, registers)

    def _render_input_registers(self, datastore: ModbusDataStore) -> None:
        offset = self._register_offset
        count = self._REGISTER_DISPLAY_COUNT
        max_addr = min(offset + count, datastore.input_registers_size)

        if offset >= datastore.input_registers_size:
            imgui.text("Offset out of range")
            return

        registers = datastore.get_input_registers(offset, max_addr - offset)
        self._render_register_table("InputRegs", offset, registers)

    def _render_register_table(
        self,
        table_id: str,
        offset: int,
        registers: List[int],
    ) -> None:
        flags = TableFlags.borders | TableFlags.row_bg
        if imgui.begin_table(table_id, 3, flags):
            try:
                imgui.table_setup_column("Address")
                imgui.table_setup_column("Decimal")
                imgui.table_setup_column("Hex")
                imgui.table_headers_row()

                for i, value in enumerate(registers):
                    imgui.table_next_row()
                    imgui.table_next_column()
                    imgui.text(f"{offset + i}")
                    imgui.table_next_column()
                    imgui.text(f"{value}")
                    imgui.table_next_column()
                    imgui.text(f"0x{value:04X}")
            finally:
                imgui.end_table()

    def _render_coils(self, datastore: ModbusDataStore) -> None:
        offset = self._register_offset
        count = self._REGISTER_DISPLAY_COUNT
        max_addr = min(offset + count, datastore.coils_size)

        if offset >= datastore.coils_size:
            imgui.text("Offset out of range")
            return

        coils = datastore.get_coils(offset, max_addr - offset)
        self._render_bool_table("Coils", offset, coils)

    def _render_discrete_inputs(self, datastore: ModbusDataStore) -> None:
        offset = self._register_offset
        count = self._REGISTER_DISPLAY_COUNT
        max_addr = min(offset + count, datastore.discrete_inputs_size)

        if offset >= datastore.discrete_inputs_size:
            imgui.text("Offset out of range")
            return

        inputs = datastore.get_discrete_inputs(offset, max_addr - offset)
        self._render_bool_table("DiscreteInputs", offset, inputs)

    def _render_bool_table(
        self,
        table_id: str,
        offset: int,
        values: List[bool],
    ) -> None:
        flags = TableFlags.borders | TableFlags.row_bg
        if imgui.begin_table(table_id, 2, flags):
            try:
                imgui.table_setup_column("Address")
                imgui.table_setup_column("Value")
                imgui.table_headers_row()

                for i, value in enumerate(values):
                    imgui.table_next_row()
                    imgui.table_next_column()
                    imgui.text(f"{offset + i}")
                    imgui.table_next_column()
                    if value:
                        self.text_success("ON")
                    else:
                        imgui.text("OFF")
            finally:
                imgui.end_table()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Menu",
                size=(self._MENU_SPLIT_X, 0),
                child_flags=self._MENU_CHILD_FLAGS,
            ):
                self._render_server_controls()
                self._render_status()
                self._render_device_list()

            imgui.same_line()

            with begin_child_context("Main"):
                if selected_config := self.selected_config:
                    self._render_device_details(selected_config)
                else:
                    text_centered("Please select a server")

        self._popups.do_process()

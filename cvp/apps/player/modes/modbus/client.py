# -*- coding: utf-8 -*-

from typing import Final, List, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import LAN_CONNECT
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.table import TableFlags
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.modbus.client import ModbusTcpClient
from cvp.modbus.config import ModbusDeviceConfig, ModbusKey
from cvp.modbus.exceptions import ModbusException
from cvp.types.override import override


class ModbusClientMode(BaseMode):
    __cvp_mode_name__ = "Modbus Client"
    __cvp_mode_icon__ = LAN_CONNECT

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS
    _REGISTER_DISPLAY_COUNT: Final[int] = 16

    def __init__(self, context: Context):
        super().__init__(context)

        self._disconnect_candidate: Optional[ModbusKey] = None
        self._confirm_disconnect = ConfirmPopup(
            title="Disconnect",
            label="Are you sure you want to disconnect this client?",
            ok="Disconnect",
            cancel="No",
            target=self.on_confirm_disconnect,
        )
        self._confirm_disconnect_all = ConfirmPopup(
            title="Disconnect All",
            label="Are you sure you want to disconnect all clients?",
            ok="Disconnect All",
            cancel="No",
            target=self.on_confirm_disconnect_all,
        )

        self._popups = PopupList(
            self._confirm_disconnect,
            self._confirm_disconnect_all,
        )

        self._register_offset: int = 0
        self._read_count: int = 16
        self._last_read_registers: List[int] = []
        self._last_read_coils: List[bool] = []
        self._last_error: Optional[str] = None

        self._write_address: int = 0
        self._write_value: int = 0
        self._write_coil_value: bool = False

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
    def selected_client(self) -> Optional[ModbusTcpClient]:
        key = self.selected_key
        if key:
            return self.modbus.get_client(key)
        return None

    def on_confirm_disconnect(self, value: bool) -> None:
        if not value:
            return
        if self._disconnect_candidate:
            self.modbus.disconnect_client(self._disconnect_candidate)
            self._disconnect_candidate = None

    def on_confirm_disconnect_all(self, value: bool) -> None:
        if not value:
            return
        for key, config in self.modbus.items():
            if config.is_client and self.modbus.has_client(key):
                self.modbus.disconnect_client(key)

    def _render_client_controls(self) -> None:
        key = self.selected_key
        config = self.selected_config
        has_selection = config is not None and config.is_client

        is_connected = False
        if key and has_selection:
            client = self.modbus.get_client(key)
            is_connected = client is not None and client.is_connected

        if is_connected:
            if button("Disconnect", disabled=not has_selection):
                self._disconnect_candidate = key
                self._confirm_disconnect.show()
        else:
            if button("Connect", disabled=not has_selection):
                if key:
                    self.modbus.connect_client(key)

        imgui.same_line()

        connected_count = sum(
            1
            for k, c in self.modbus.items()
            if c.is_client and self.modbus.has_client(k)
        )

        if button("Disconnect All", disabled=connected_count == 0):
            self._confirm_disconnect_all.show()

    def _render_status(self) -> None:
        imgui.separator()

        client_count = sum(1 for _, c in self.modbus.items() if c.is_client)
        connected_count = sum(
            1
            for k, c in self.modbus.items()
            if c.is_client and self.modbus.has_client(k)
        )

        imgui.text(f"Clients: {connected_count}/{client_count} connected")
        imgui.separator()

    def _render_device_list(self) -> None:
        if imgui.begin_list_box("##ClientList", FIT_SIZE):
            try:
                for key, config in self.modbus.items():
                    if not config.is_client:
                        continue

                    client = self.modbus.get_client(key)
                    is_connected = client is not None and client.is_connected
                    status = "[C]" if is_connected else "[D]"
                    label = f"{status} {config.name}"

                    selected = str(key) == self.selected_submenu
                    if imgui.selectable(label, selected)[1]:
                        self.selected_submenu = str(key)
                        self._last_read_registers = []
                        self._last_read_coils = []
                        self._last_error = None
            finally:
                imgui.end_list_box()

    def _render_client_details(self, config: ModbusDeviceConfig) -> None:
        imgui.text(f"Name: {config.name}")
        imgui.text(f"Host: {config.host}")
        imgui.text(f"Port: {config.port}")
        imgui.text(f"Unit ID: {config.unit_id}")
        imgui.text(f"Timeout: {config.timeout}s")

        client = self.selected_client

        imgui.separator()

        if client and client.is_connected:
            self.text_success("Status: Connected")
        elif client and client.is_running:
            self.text_warning("Status: Reconnecting...")
        else:
            self.text_warning("Status: Disconnected")

        imgui.separator()

        if client and client.is_connected:
            self._render_read_write_controls(client)

    def _render_read_write_controls(self, client: ModbusTcpClient) -> None:
        if imgui.begin_tab_bar("##ClientTabs"):
            try:
                if imgui.begin_tab_item("Read Registers")[0]:
                    self._render_read_registers_tab(client)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Read Coils")[0]:
                    self._render_read_coils_tab(client)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Write Register")[0]:
                    self._render_write_register_tab(client)
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Write Coil")[0]:
                    self._render_write_coil_tab(client)
                    imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()

    def _render_read_registers_tab(self, client: ModbusTcpClient) -> None:
        _, self._register_offset = imgui.input_int(
            "Start Address",
            self._register_offset,
            step=1,
        )
        self._register_offset = max(0, min(65535, self._register_offset))

        _, self._read_count = imgui.input_int(
            "Count",
            self._read_count,
            step=1,
        )
        self._read_count = max(1, min(125, self._read_count))

        if button("Read Holding"):
            self._do_read_holding_registers(client)

        imgui.same_line()

        if button("Read Input"):
            self._do_read_input_registers(client)

        if self._last_error:
            imgui.separator()
            self.text_error(f"Error: {self._last_error}")

        if self._last_read_registers:
            imgui.separator()
            self._render_register_table(
                "ReadRegs",
                self._register_offset,
                self._last_read_registers,
            )

    def _render_read_coils_tab(self, client: ModbusTcpClient) -> None:
        _, self._register_offset = imgui.input_int(
            "Start Address##coils",
            self._register_offset,
            step=1,
        )
        self._register_offset = max(0, min(65535, self._register_offset))

        _, self._read_count = imgui.input_int(
            "Count##coils",
            self._read_count,
            step=1,
        )
        self._read_count = max(1, min(2000, self._read_count))

        if button("Read Coils"):
            self._do_read_coils(client)

        imgui.same_line()

        if button("Read Discrete Inputs"):
            self._do_read_discrete_inputs(client)

        if self._last_error:
            imgui.separator()
            self.text_error(f"Error: {self._last_error}")

        if self._last_read_coils:
            imgui.separator()
            self._render_bool_table(
                "ReadCoils",
                self._register_offset,
                self._last_read_coils,
            )

    def _render_write_register_tab(self, client: ModbusTcpClient) -> None:
        _, self._write_address = imgui.input_int(
            "Address##writereg",
            self._write_address,
            step=1,
        )
        self._write_address = max(0, min(65535, self._write_address))

        _, self._write_value = imgui.input_int(
            "Value##writereg",
            self._write_value,
            step=1,
        )
        self._write_value = max(0, min(65535, self._write_value))

        imgui.text(f"Hex: 0x{self._write_value:04X}")

        if button("Write Single Register"):
            self._do_write_single_register(client)

        if self._last_error:
            imgui.separator()
            self.text_error(f"Error: {self._last_error}")

    def _render_write_coil_tab(self, client: ModbusTcpClient) -> None:
        _, self._write_address = imgui.input_int(
            "Address##writecoil",
            self._write_address,
            step=1,
        )
        self._write_address = max(0, min(65535, self._write_address))

        _, self._write_coil_value = imgui.checkbox(
            "Value (ON/OFF)",
            self._write_coil_value,
        )

        if button("Write Single Coil"):
            self._do_write_single_coil(client)

        if self._last_error:
            imgui.separator()
            self.text_error(f"Error: {self._last_error}")

    def _do_read_holding_registers(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        self._last_read_registers = []
        try:
            self._last_read_registers = client.read_holding_registers(
                self._register_offset,
                self._read_count,
            )
        except ModbusException as e:
            self._last_error = str(e)

    def _do_read_input_registers(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        self._last_read_registers = []
        try:
            self._last_read_registers = client.read_input_registers(
                self._register_offset,
                self._read_count,
            )
        except ModbusException as e:
            self._last_error = str(e)

    def _do_read_coils(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        self._last_read_coils = []
        try:
            self._last_read_coils = client.read_coils(
                self._register_offset,
                self._read_count,
            )
        except ModbusException as e:
            self._last_error = str(e)

    def _do_read_discrete_inputs(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        self._last_read_coils = []
        try:
            self._last_read_coils = client.read_discrete_inputs(
                self._register_offset,
                self._read_count,
            )
        except ModbusException as e:
            self._last_error = str(e)

    def _do_write_single_register(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        try:
            client.write_single_register(self._write_address, self._write_value)
        except ModbusException as e:
            self._last_error = str(e)

    def _do_write_single_coil(self, client: ModbusTcpClient) -> None:
        self._last_error = None
        try:
            client.write_single_coil(self._write_address, self._write_coil_value)
        except ModbusException as e:
            self._last_error = str(e)

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
                self._render_client_controls()
                self._render_status()
                self._render_device_list()

            imgui.same_line()

            with begin_child_context("Main"):
                if selected_config := self.selected_config:
                    self._render_client_details(selected_config)
                else:
                    text_centered("Please select a client")

        self._popups.do_process()

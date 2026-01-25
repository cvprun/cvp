# -*- coding: utf-8 -*-

from typing import Dict, Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import MEMORY
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.table import TableFlags
from cvp.imgui.flags.table_column import WIDTH_FIXED
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.text_centered import text_centered
from cvp.modbus.config import ModbusDataStoreConfig, ModbusDeviceConfig, ModbusKey
from cvp.types.override import override


class ModbusMode(BaseMode):
    __cvp_mode_name__ = "Modbus"
    __cvp_mode_icon__ = MEMORY

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

        self._stop_candidate: Optional[ModbusKey] = None
        self._remove_candidate: Optional[ModbusKey] = None

        self._input_new_server = InputTextPopup(
            title="New Server",
            label="Enter server name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_server,
        )
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
        self._confirm_remove = ConfirmPopup(
            title="Remove Server",
            label="Are you sure you want to remove this server?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self._popups = PopupList(
            self._input_new_server,
            self._confirm_stop,
            self._confirm_stop_all,
            self._confirm_remove,
        )

        self._new_address: int = 0
        self._new_register_value: int = 0
        self._new_bool_value: bool = False

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
    def selected_datastore_config(self) -> Optional[ModbusDataStoreConfig]:
        key = self.selected_key
        if key:
            return self.modbus.get_datastore_config(key)
        return None

    def _ensure_datastore_config(self) -> Optional[ModbusDataStoreConfig]:
        key = self.selected_key
        if not key:
            return None

        config = self.modbus.get_datastore_config(key)
        if config is None:
            config = ModbusDataStoreConfig(uuid=str(key))
            self.modbus._datastore_configs[key] = config
        return config

    def on_new_server(self, name: str) -> None:
        if not name:
            return
        from cvp.modbus.config import ModbusRole

        self.modbus.add_device(
            name=name,
            role=ModbusRole.server,
        )

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

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        if self._remove_candidate:
            self.modbus.remove_device(self._remove_candidate)
            if str(self._remove_candidate) == self.selected_submenu:
                self.selected_submenu = str()
            self._remove_candidate = None

    def _render_server_controls(self) -> None:
        key = self.selected_key
        config = self.selected_config
        has_selection = config is not None and config.is_server

        if button("New"):
            self._input_new_server.text = ""
            self._input_new_server.show()

        imgui.same_line()

        can_delete = has_selection and not self.modbus.has_server(key)
        if button("Del", disabled=not can_delete):
            self._remove_candidate = key
            self._confirm_remove.show()

        imgui.same_line()

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
                    display_name = config.name if config.name else "(unnamed)"
                    label = f"{status} {display_name}"

                    selected = str(key) == self.selected_submenu
                    if imgui.selectable(label, selected)[1]:
                        self.selected_submenu = str(key)
            finally:
                imgui.end_list_box()

    def _render_device_details(self, config: ModbusDeviceConfig) -> None:
        key = config.key
        server = self.modbus.get_server(key)
        is_running = server is not None and server.is_running

        imgui.begin_disabled(disabled=is_running)
        try:
            self._render_config_editor(config)
        finally:
            imgui.end_disabled()

        imgui.separator()

        if is_running:
            self.text_success("Status: Running")
            imgui.text(f"Connected Clients: {server.client_count}")
        else:
            self.text_warning("Status: Stopped")

        imgui.separator()
        self._render_datastore_config_editor()

    def _render_config_editor(self, config: ModbusDeviceConfig) -> None:
        if name := input_text("Name", config.name):
            config.name = name.value

        if host := input_text("Host", config.host):
            config.host = host.value

        if port := input_int("Port", config.port):
            config.port = max(1, min(65535, port.value))

        if unit_id := input_int("Unit ID", config.unit_id):
            config.unit_id = max(1, min(255, unit_id.value))

        if autostart := checkbox("Autostart", config.autostart):
            config.autostart = autostart.state

    def _render_datastore_config_editor(self) -> None:
        imgui.text("Data Store Configuration")
        imgui.separator()

        if imgui.begin_tab_bar("##DatastoreConfigTabs"):
            try:
                if imgui.begin_tab_item("Holding Registers")[0]:
                    self._render_register_editor("holding_registers")
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Input Registers")[0]:
                    self._render_register_editor("input_registers")
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Coils")[0]:
                    self._render_bool_editor("coils")
                    imgui.end_tab_item()

                if imgui.begin_tab_item("Discrete Inputs")[0]:
                    self._render_bool_editor("discrete_inputs")
                    imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()

    def _render_register_editor(self, store_name: str) -> None:
        ds_config = self._ensure_datastore_config()
        if ds_config is None:
            imgui.text("No configuration available")
            return

        data: Dict[int, int] = getattr(ds_config, store_name)

        imgui.text("Add Entry:")
        imgui.set_next_item_width(100)
        _, self._new_address = imgui.input_int("Address##reg", self._new_address, 0, 0)
        self._new_address = max(0, min(65535, self._new_address))

        imgui.same_line()
        imgui.set_next_item_width(100)
        _, self._new_register_value = imgui.input_int(
            "Value##reg", self._new_register_value, 0, 0
        )
        self._new_register_value = max(0, min(65535, self._new_register_value))

        imgui.same_line()
        if button("Add##reg"):
            data[self._new_address] = self._new_register_value
            self._sync_to_datastore(store_name, self._new_address)

        imgui.separator()

        if not data:
            imgui.text("No entries. Add entries above.")
            return

        flags = TableFlags.borders | TableFlags.row_bg
        if imgui.begin_table(f"##{store_name}", 4, flags):
            try:
                imgui.table_setup_column("Address", WIDTH_FIXED, 80)
                imgui.table_setup_column("Decimal", WIDTH_FIXED, 80)
                imgui.table_setup_column("Hex", WIDTH_FIXED, 80)
                imgui.table_setup_column("Actions", WIDTH_FIXED, 100)
                imgui.table_headers_row()

                to_delete = None
                for addr in sorted(data.keys()):
                    value = data[addr]
                    imgui.table_next_row()

                    imgui.table_next_column()
                    imgui.text(f"{addr}")

                    imgui.table_next_column()
                    imgui.push_id(f"val_{addr}")
                    imgui.set_next_item_width(60)
                    changed, new_val = imgui.input_int("##v", value, 0, 0)
                    if changed:
                        new_val = max(0, min(65535, new_val))
                        data[addr] = new_val
                        self._sync_to_datastore(store_name, addr)
                    imgui.pop_id()

                    imgui.table_next_column()
                    imgui.text(f"0x{value:04X}")

                    imgui.table_next_column()
                    imgui.push_id(f"del_{addr}")
                    if button("Del"):
                        to_delete = addr
                    imgui.pop_id()

                if to_delete is not None:
                    del data[to_delete]
            finally:
                imgui.end_table()

    def _render_bool_editor(self, store_name: str) -> None:
        ds_config = self._ensure_datastore_config()
        if ds_config is None:
            imgui.text("No configuration available")
            return

        data: Dict[int, bool] = getattr(ds_config, store_name)

        imgui.text("Add Entry:")
        imgui.set_next_item_width(100)
        _, self._new_address = imgui.input_int("Address##bool", self._new_address, 0, 0)
        self._new_address = max(0, min(65535, self._new_address))

        imgui.same_line()
        _, self._new_bool_value = imgui.checkbox("Value##bool", self._new_bool_value)

        imgui.same_line()
        if button("Add##bool"):
            data[self._new_address] = self._new_bool_value
            self._sync_to_datastore(store_name, self._new_address)

        imgui.separator()

        if not data:
            imgui.text("No entries. Add entries above.")
            return

        flags = TableFlags.borders | TableFlags.row_bg
        if imgui.begin_table(f"##{store_name}", 3, flags):
            try:
                imgui.table_setup_column("Address", WIDTH_FIXED, 80)
                imgui.table_setup_column("Value", WIDTH_FIXED, 80)
                imgui.table_setup_column("Actions", WIDTH_FIXED, 100)
                imgui.table_headers_row()

                to_delete = None
                for addr in sorted(data.keys()):
                    value = data[addr]
                    imgui.table_next_row()

                    imgui.table_next_column()
                    imgui.text(f"{addr}")

                    imgui.table_next_column()
                    imgui.push_id(f"chk_{addr}")
                    changed, new_val = imgui.checkbox("##c", value)
                    if changed:
                        data[addr] = new_val
                        self._sync_to_datastore(store_name, addr)
                    imgui.same_line()
                    if new_val:
                        self.text_success("ON")
                    else:
                        imgui.text("OFF")
                    imgui.pop_id()

                    imgui.table_next_column()
                    imgui.push_id(f"del_{addr}")
                    if button("Del"):
                        to_delete = addr
                    imgui.pop_id()

                if to_delete is not None:
                    del data[to_delete]
            finally:
                imgui.end_table()

    def _sync_to_datastore(self, store_name: str, addr: int) -> None:
        key = self.selected_key
        if not key:
            return

        datastore = self.modbus.get_datastore(key)
        if datastore is None:
            return

        ds_config = self.modbus.get_datastore_config(key)
        if ds_config is None:
            return

        data = getattr(ds_config, store_name)
        if addr not in data:
            return

        value = data[addr]

        if store_name == "holding_registers":
            datastore.set_holding_register(addr, value)
        elif store_name == "input_registers":
            datastore.set_input_registers(addr, [value])
        elif store_name == "coils":
            datastore.set_coil(addr, value)
        elif store_name == "discrete_inputs":
            datastore.set_discrete_inputs(addr, [value])

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

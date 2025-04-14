# -*- coding: utf-8 -*-

from ipaddress import IPv4Address, IPv6Address

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.logging.logging import logger
from cvp.popups.confirm import ConfirmPopup
from cvp.types.override import override
from cvp.variables import (
    SIDE_MENU_WIDTH,
    WSD_NAME_DEFAULT,
    WSD_ONVIF_SCOPE_PREFIX,
    WSD_ONVIF_SCOPE_PREFIX_LEN,
)
from cvp.wsdiscovery.manager import WsDiscoveryFilename
from cvp.wsdiscovery.wsd import WsDiscovery
from wsdiscovery import WSDiscovery


class WsDiscoveryMode(BaseMode):
    __cvp_mode_name__ = "WsDiscovery"

    def __init__(self, context: Context):
        super().__init__(context)
        self._wsd_running = False
        self._remove_candidate = WsDiscoveryFilename(str())
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove device?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

    @property
    def wsdiscovery(self):
        return self.context.wsdiscovery

    @property
    def config(self):
        return self.context.config.wsdiscovery

    @property
    def selected(self) -> WsDiscoveryFilename:
        return WsDiscoveryFilename(self.config.selected)

    @selected.setter
    def selected(self, value: WsDiscoveryFilename) -> None:
        self.config.selected = str(value)

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.wsdiscovery
        self.wsdiscovery.remove(self._remove_candidate)

    def run_discovery(self) -> None:
        if self._wsd_running:
            raise ValueError("WsDiscovery is already running")

        try:
            self.context.pm.submit_thread(self._discovery_main)
        except BaseException as e:
            logger.exception(e)
            self.context.mq.append_toast(f"Discovery failed: '{e}'")
            self._wsd_running = False
        else:
            self._wsd_running = True

    def _discovery_main(self) -> None:
        try:
            wsd = WSDiscovery()
            wsd.start()
            try:
                for service in wsd.searchServices():
                    item = WsDiscovery()
                    item.epr = service.getEPR()
                    item.instance_id = service.getInstanceId()
                    item.message_number = service.getMessageNumber()
                    item.metadata_version = service.getMetadataVersion()
                    item.scopes = [s.getValue() for s in service.getScopes()]
                    item.types = [t.getFullname() for t in service.getTypes()]
                    item.xaddrs = [a for a in service.getXAddrs()]
                    item.error = str()

                    for scope in item.scopes:
                        assert isinstance(scope, str)
                        if scope.startswith(WSD_ONVIF_SCOPE_PREFIX):
                            item.name = scope[WSD_ONVIF_SCOPE_PREFIX_LEN:]

                    if not item.name:
                        item.name = item.epr
                    if not item.name:
                        item.name = WSD_NAME_DEFAULT

                    logger.info(f"Device discovered: {item}")
                    self.wsdiscovery.add(item)
            finally:
                wsd.stop()
        finally:
            self.wsdiscovery.write_all_files()
            self._wsd_running = False

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        split_x=SIDE_MENU_WIDTH,
        menu_child_flags=RESIZE_X | BORDERS,
    ) -> None:
        running = bool(self._wsd_running)
        with begin_child_context("Menu", split_x, child_flags=menu_child_flags):
            if running:
                imgui.begin_disabled()
            try:
                self.do_discovery_process()
                imgui.separator()
                if button("Reload"):
                    self.wsdiscovery.reload_all_files()
                imgui.same_line()
                if button("Del", disabled=self.selected not in self.wsdiscovery):
                    self._remove_candidate = self.selected
                    self._confirm_remove.show()
            finally:
                if running:
                    imgui.end_disabled()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for filename, wsd in self.wsdiscovery.items():
                        label = f"{wsd.name}###{filename}"
                        selected = filename == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_wsd := self.wsdiscovery.get(self.selected):
                self.do_wsdiscovery_process(selected_wsd)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()

    def do_discovery_process(self) -> None:
        imgui.text("Web Services Dynamic Discovery")
        imgui.separator()

        imgui.text("Protocol")
        if imgui.radio_button("TCP", self.config.is_tcp):
            self.config.set_tcp()
        imgui.same_line()
        if imgui.radio_button("UDP", self.config.is_udp):
            self.config.set_udp()

        ipv4_result = input_text("IPv4", self.config.ipv4_address, ENTER_RETURNS_TRUE)
        if ipv4_result.changed:
            try:
                IPv4Address(ipv4_result.value)
            except:  # noqa
                pass
            else:
                self.config.ipv4_address = ipv4_result.value

        ipv6_result = input_text("IPv6", self.config.ipv6_address, ENTER_RETURNS_TRUE)
        if ipv6_result.changed:
            try:
                IPv6Address(ipv6_result.value)
            except:  # noqa
                pass
            else:
                self.config.ipv6_address = ipv6_result.value

        if port_result := input_int("Port", self.config.port):
            self.config.port = port_result.value

        if timeout_result := input_float("Timeout", self.config.timeout):
            self.config.timeout = timeout_result.value

        if button("Reset Default"):
            self.config.reset_defaults()
        if button("Discovery"):
            self.run_discovery()

    def do_wsdiscovery_process(self, wsd: WsDiscovery) -> None:
        wsd.name = input_text_value("Name", wsd.name)
        input_text_disabled("EPR", wsd.epr)
        input_text_disabled("InstanceID", str(wsd.instance_id))
        input_text_disabled("MessageNumber", str(wsd.message_number))
        input_text_disabled("MetadataVersion", str(wsd.metadata_version))

        imgui.text("Types:")
        if wsd.types:
            for i, type_ in enumerate(wsd.types):
                imgui.bullet()
                imgui.same_line()
                input_text_disabled(f"##Type[{i}]", type_)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty types")

        imgui.text("Scopes:")
        if wsd.scopes:
            for i, scope in enumerate(wsd.scopes):
                imgui.bullet()
                imgui.same_line()
                input_text_disabled(f"##Scope[{i}]", scope)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty scopes")

        imgui.text("XAddr:")
        if wsd.xaddrs:
            has_onvif_scope = wsd.has_onvif_scope
            for i, xaddr in enumerate(wsd.xaddrs):
                imgui.bullet()

                if has_onvif_scope:
                    imgui.same_line()
                    if imgui.button(f"Use ONVIF## Use ONVIF[{i}]"):
                        config = OnvifConfig(address=xaddr, name=wsd.name)
                        self.context.config.onvifs.append(config)

                imgui.same_line()
                input_text_disabled(f"##XAddr[{i}]", xaddr)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty xaddrs")

# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Final, Optional

from imgui_bundle import imgui
from wsdiscovery import WSDiscovery

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
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
from cvp.imgui.spinner import spinner
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.logging.logging import logger
from cvp.net.address_family import is_ip_address
from cvp.popups.confirm import ConfirmPopup
from cvp.types.override import override
from cvp.variables import (
    WSD_IPV4_MULTICAST_ADDRESS,
    WSD_IPV6_MULTICAST_ADDRESS,
    WSD_MULTICAST_UDP_REPEAT,
    WSD_NAME_DEFAULT,
    WSD_ONVIF_SCOPE_PREFIX,
    WSD_ONVIF_SCOPE_PREFIX_LEN,
    WSD_PORT_NUMBER,
    WSD_RELATES_TO,
    WSD_UNICAST_UDP_REPEAT,
)
from cvp.wsdiscovery.wsd import WsDiscovery

_MENU_SPLIT_X: Final[int] = 300
_MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS


class WsDiscoveryMode(BaseMode):
    __cvp_mode_name__ = "WsDiscovery"

    def __init__(self, context: Context):
        super().__init__(context)
        self._discovery_runner = context.pm.create_thread_runner(self.on_discovery_main)
        self._discovery_begin = datetime.now().astimezone()
        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove device?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all devices?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def wsdiscovery(self):
        return self.context.wsdiscovery

    @property
    def config(self):
        return self.context.config.wsdiscovery

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def run_discovery(self) -> None:
        if self._discovery_runner.running:
            raise ValueError("WsDiscovery is already running")

        try:
            self._discovery_runner(
                self.config.address if self.config.is_unicast else None,
                self.config.port if self.config.is_unicast else None,
                self.config.timeout,
                self.config.multicast_repeat,
                self.config.unicast_repeat,
                self.config.relates_to,
            )
            self._discovery_begin = datetime.now().astimezone()
        except BaseException as e:
            logger.exception(e)
            self.context.toast(f"Discovery failed: '{e}'")

    def on_discovery_main(
        self,
        address: Optional[None] = None,
        port: Optional[int] = None,
        timeout: Optional[int] = None,
        multicast_repeat=WSD_MULTICAST_UDP_REPEAT,
        unicast_repeat=WSD_UNICAST_UDP_REPEAT,
        relates_to=WSD_RELATES_TO,
    ) -> None:
        wsd = WSDiscovery(
            unicast_num=unicast_repeat,
            multicast_num=multicast_repeat,
            relates_to=relates_to,
        )
        wsd.start()
        try:
            for service in wsd.searchServices(
                address=address,
                port=port,
                timeout=timeout,
            ):
                epr = service.getEPR()
                item = self.wsdiscovery.get(epr, WsDiscovery(epr))
                assert item.epr == epr
                item.instance_id = service.getInstanceId()
                item.message_number = service.getMessageNumber()
                item.metadata_version = service.getMetadataVersion()
                item.scopes = [s.getValue() for s in service.getScopes()]
                item.types = [t.getFullname() for t in service.getTypes()]
                item.xaddrs = [a for a in service.getXAddrs()]
                item.error = str()
                item.created_at = datetime.now().astimezone()

                if not item.name:
                    for scope in item.scopes:
                        assert isinstance(scope, str)
                        if scope.startswith(WSD_ONVIF_SCOPE_PREFIX):
                            item.name = scope[WSD_ONVIF_SCOPE_PREFIX_LEN:]
                    if not item.name:
                        item.name = item.epr
                    if not item.name:
                        item.name = WSD_NAME_DEFAULT

                logger.info(f"Device discovered: {item}")
                self.wsdiscovery.add(epr, item)
        finally:
            wsd.stop()

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.wsdiscovery
        self.wsdiscovery.remove(self._remove_candidate)

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.wsdiscovery.remove_all()

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
        menu_split_x=_MENU_SPLIT_X,
        menu_child_flags=_MENU_CHILD_FLAGS,
    ) -> None:
        running = self._discovery_runner.running
        with begin_child_context("Menu", menu_split_x, child_flags=menu_child_flags):
            if running:
                imgui.begin_disabled()
            try:
                self.do_discovery_process(running=running)
            finally:
                if running:
                    imgui.end_disabled()

            imgui.separator()
            if button("Reload", disabled=running):
                self.wsdiscovery.read_all_config_files()
            imgui.same_line()
            if button("Del", disabled=self.selected not in self.wsdiscovery):
                self._remove_candidate = self.selected
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=running or not self.wsdiscovery):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, wsd in self.wsdiscovery.items():
                        label = f"{wsd.name}###{key}"
                        selected = key == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_wsd := self.wsdiscovery.get(self.selected):
                self.do_wsdiscovery_process(selected_wsd)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()
        self._confirm_clear.do_process()

    def do_discovery_process(self, running: bool) -> None:
        imgui.text("Web Services Dynamic Discovery")
        imgui.separator()

        if imgui.radio_button("Multicast", self.config.is_multicast):
            self.config.set_multicast()
        imgui.same_line()
        if imgui.radio_button("Unicast", self.config.is_unicast):
            self.config.set_unicast()

        if self.config.is_multicast:
            input_text_disabled("IPv4", WSD_IPV4_MULTICAST_ADDRESS)
            input_text_disabled("IPv6", WSD_IPV6_MULTICAST_ADDRESS)
            input_text_disabled("Port", str(WSD_PORT_NUMBER))

            if repeat_result := input_int("Repeat", self.config.multicast_repeat):
                self.config.multicast_repeat = repeat_result.value
            hovered_tooltip_text("Number of Multicast messages to send")
        elif self.config.is_unicast:
            addr_result = input_text("Address", self.config.address, ENTER_RETURNS_TRUE)
            if addr_result.changed and is_ip_address(addr_result.value):
                self.config.address = addr_result.value
            if port_result := input_int("Port", self.config.port):
                self.config.port = port_result.value

            if repeat_result := input_int("Repeat", self.config.unicast_repeat):
                self.config.unicast_repeat = repeat_result.value
            hovered_tooltip_text("Number of Unicast messages to send")
        else:
            assert False, "Inaccessible section"

        if timeout_result := input_float("Timeout", self.config.timeout, step=1.0):
            self.config.timeout = timeout_result.value
        hovered_tooltip_text("Discovery timeout in seconds")

        if relates_to_result := checkbox("RelatesTo", self.config.relates_to):
            self.config.relates_to = relates_to_result.state
        hovered_tooltip_text("Also use RelatesTo tag to recognize incoming messages")

        if button("Reset Default"):
            self.config.reset_defaults()

        if button("Discovery", disabled=running):
            self.run_discovery()

        if running:
            imgui.same_line()
            spinner("Running Spinner")

            imgui.same_line()
            duration = datetime.now().astimezone() - self._discovery_begin
            remain_seconds = self.config.timeout - duration.total_seconds()
            imgui.text(f"{remain_seconds:.01f}s")

    def do_wsdiscovery_process(self, wsd: WsDiscovery) -> None:
        wsd.name = input_text_value("Name", wsd.name)

        input_text_disabled("EndPoint Reference", wsd.epr)
        input_text_disabled("Instance ID", str(wsd.instance_id))
        input_text_disabled("Message Number", str(wsd.message_number))
        input_text_disabled("Metadata Version", str(wsd.metadata_version))
        input_text_disabled("Created At", wsd.created_at.isoformat())

        if wsd.has_error:
            imgui.text_colored(self.error_color, wsd.error)

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
                        self.context.onvifs.add_config(name=wsd.name, address=xaddr)

                imgui.same_line()
                input_text_disabled(f"##XAddr[{i}]", xaddr)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty xaddrs")

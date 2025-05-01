# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.vms.onvif._base import BaseOnvifTab
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.onvif.config import OnvifConfig
from cvp.types.override import override


class OnvifInfoTab(BaseOnvifTab):
    __cvp_onvif_tab_name__ = "Info"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self, onvif: OnvifConfig) -> None:
        input_text_disabled("UUID", onvif.key)
        onvif.name = input_text_value("Name", onvif.name)
        onvif.address = input_text_value("Address", onvif.address)

        ssl_verify = imgui.checkbox("No SSL Verify", onvif.no_verify)
        ssl_verify_changed = ssl_verify[0]
        ssl_verify_value = ssl_verify[1]
        assert isinstance(ssl_verify_changed, bool)
        assert isinstance(ssl_verify_value, bool)
        if ssl_verify_changed:
            onvif.no_verify = ssl_verify_value

        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text(
                        "Skip the certificate verification process."
                        " This may be a temporary solution if you get a"
                        " 'certificate verify failed' error."
                    )
                finally:
                    imgui.end_tooltip()

        same_host = imgui.checkbox("Same host", onvif.same_host)
        same_host_changed = same_host[0]
        same_host_value = same_host[1]
        assert isinstance(same_host_changed, bool)
        assert isinstance(same_host_value, bool)
        if same_host_changed:
            onvif.same_host = same_host_value

        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text(
                        "Prevents WSDL addresses from being incorrect when accessing"
                        " ONVIF devices in environments such as proxy or tunneling."
                    )
                finally:
                    imgui.end_tooltip()

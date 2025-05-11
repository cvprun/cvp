# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.vms.onvif._base import BaseOnvifTab
from cvp.context.context import Context
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE, PASSWORD
from cvp.imgui.input_text_value import input_text_value
from cvp.onvif.config import OnvifConfig
from cvp.types.override import override


class OnvifAuthTab(BaseOnvifTab):
    __cvp_onvif_tab_name__ = "Auth"

    def __init__(self, context: Context):
        super().__init__(context)
        self._show_password = False

    @override
    def on_process(self, onvif: OnvifConfig) -> None:
        use_wsse = imgui.checkbox("Use WS-Security", onvif.use_wsse)
        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text("Use <wsse:UsernameToken> in <soap:Header>")
                finally:
                    imgui.end_tooltip()
        use_wsse_changed = use_wsse[0]
        use_wsse_value = use_wsse[1]
        assert isinstance(use_wsse_changed, bool)
        assert isinstance(use_wsse_value, bool)
        if use_wsse_changed:
            onvif.use_wsse = use_wsse_value

        if not onvif.use_wsse:
            return

        onvif.username = input_text_value("Username", onvif.username)

        password_flags = ENTER_RETURNS_TRUE if self._show_password else PASSWORD
        prev_password = self.context.keyring.onvif.get_or_empty(onvif.key)
        next_password = input_text_value("Password", prev_password, password_flags)
        if prev_password != next_password:
            self.context.keyring.onvif.set(onvif.key, next_password)

        show_password = imgui.checkbox("Show Password", self._show_password)
        show_password_changed = show_password[0]
        show_password_value = show_password[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_password = show_password_value

        imgui.text("HTTP Authorization header:")
        if imgui.radio_button("None", onvif.http_auth is None):
            onvif.http_auth = None
        imgui.same_line()
        if imgui.radio_button("Basic", onvif.is_http_basic):
            onvif.set_http_basic()
        imgui.same_line()
        if imgui.radio_button("Digest", onvif.is_http_digest):
            onvif.set_http_digest()

        imgui.text("Password Type:")

        if imgui.radio_button("PasswordText", not onvif.encode_digest):
            onvif.encode_digest = False
        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text('Use <wsse:Password Type="wsse:PasswordText">')
                finally:
                    imgui.end_tooltip()

        imgui.same_line()
        if imgui.radio_button("PasswordDigest", onvif.encode_digest):
            onvif.encode_digest = True
        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text('Use <wsse:Password Type="wsse:PasswordDigest">')
                finally:
                    imgui.end_tooltip()
